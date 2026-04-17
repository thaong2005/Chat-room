from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form, Response, Cookie
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import urllib

from .db import get_recent_messages, init_db, save_message, create_user, verify_user
from .filter.profanity_filter import AntlrWordFilter, load_bad_words

MAX_MESSAGE_LENGTH = 500


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: set[WebSocket] = set()
        self.usernames: dict[WebSocket, str] = {}
        self.typing_users: set[str] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        self.connections.discard(websocket)
        username = self.usernames.pop(websocket, None)
        if username and username in self.typing_users:
            self.typing_users.remove(username)
            await self.broadcast_typing_users()
        await self.broadcast_user_list()

    async def register_username(self, websocket: WebSocket, requested_name: str) -> str:
        base = requested_name.strip()[:24] or "Guest"
        existing = set(self.usernames.values())
        candidate = base
        suffix = 2
        while candidate in existing:
            candidate = f"{base}{suffix}"
            suffix += 1

        self.usernames[websocket] = candidate
        await self.broadcast_user_list()
        return candidate

    async def broadcast(self, payload: dict[str, Any]) -> None:
        dead_connections: list[WebSocket] = []
        for connection in self.connections:
            try:
                await connection.send_json(payload)
            except Exception:
                dead_connections.append(connection)

        for dead in dead_connections:
            await self.disconnect(dead)

    async def broadcast_user_list(self) -> None:
        users = sorted(self.usernames.values(), key=lambda value: value.lower())
        await self.broadcast({"type": "users", "users": users})

    async def broadcast_typing_users(self) -> None:
        users = sorted(self.typing_users, key=lambda value: value.lower())
        await self.broadcast({"type": "typing", "users": users})


app = FastAPI(title="Chatroom MVP")
manager = ConnectionManager()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DIR = PROJECT_ROOT / "frontend" / "public"
BAD_WORDS_FILE = Path(__file__).resolve().parent / "filter" / "bad_words.txt"

word_filter = AntlrWordFilter(load_bad_words(BAD_WORDS_FILE))

if PUBLIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=PUBLIC_DIR), name="static")


@app.on_event("startup")
async def startup_event() -> None:
    init_db()



@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def index(chat_session: Optional[str] = Cookie(None)):
    # check for cookie "chat_session", redirect to login if there isn't
    if not chat_session:
        return RedirectResponse(url="/login")

    return FileResponse(PUBLIC_DIR / "index.html")

@app.get("/login")
async def login() -> FileResponse:
    return FileResponse(PUBLIC_DIR / "loginPage.html")

@app.get("/register")
async def register() -> FileResponse:
    return FileResponse(PUBLIC_DIR / "registerPage.html")

@app.get("/styles.css")
async def styles() -> FileResponse:
    return FileResponse(PUBLIC_DIR / "styles.css")

@app.get("/app.js")
async def app_js() -> FileResponse:
    return FileResponse(PUBLIC_DIR / "app.js")

@app.get("/checkMessage.js")
async def checkMessage_js() -> FileResponse:
    return FileResponse(PUBLIC_DIR / "checkMessage.js")

@app.post("/register")
async def handle_register(username: str = Form(...), password: str = Form(...)):
    success = create_user(username, password)
    if success:
        # After register, redirect to login page
        msg = urllib.parse.quote("Account created! Redirecting to login...")

        return RedirectResponse(url=f"/login?msg={msg}", status_code=303)
    else:
        msg = urllib.parse.quote("Username already exists.")
        return RedirectResponse(url=f"/register?error={msg}", status_code=303)


@app.post("/login")
async def handle_login(response: Response, username: str = Form(...), password: str = Form(...)):
    is_valid = verify_user(username, password)
    if is_valid:

        res = RedirectResponse(url="/", status_code=303)

        res.set_cookie(
            key="chat_session",
            value=username,
            httponly=True,
            max_age=3600
        )

        return res
    else:
        msg = urllib.parse.quote("Invalid credentials. Please try again.")
        return RedirectResponse(url=f"/login?error={msg}", status_code=303)


@app.post("/logout")
async def logout():
    res = RedirectResponse(url="/login", status_code=303)
    
    res.delete_cookie("chat_session")
    
    return res

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    raw_username = websocket.cookies.get("chat_session")

    if not raw_username:
        await websocket.close(code=1008) # if not logged  in, close socket
        return
    
    await manager.connect(websocket)

    username = await manager.register_username(websocket, raw_username)

    try:

        await websocket.send_json({
            "type": "joined",
            "username": username,
            "history": get_recent_messages(100),
        })

        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")

            if event_type == "join":
                username = await manager.register_username(
                    websocket,
                    str(data.get("username", "")),
                )
                await websocket.send_json({
                    "type": "joined",
                    "username": username,
                    "history": get_recent_messages(100),
                })
                await manager.broadcast(
                    {
                        "type": "system",
                        "content": f"{username} joined the room.",
                    }
                )
                continue

            username = manager.usernames.get(websocket)
            if not username:
                await websocket.send_json(
                    {"type": "error", "message": "Join before sending events."}
                )
                continue

            if event_type == "message":
                content = str(data.get("content", "")).strip()
                if not content:
                    continue
                if len(content) > MAX_MESSAGE_LENGTH:
                    await websocket.send_json(
                        {
                            "type": "error",
                            "message": f"Message too long (max {MAX_MESSAGE_LENGTH} chars).",
                        }
                    )
                    continue

                if username in manager.typing_users:
                    manager.typing_users.remove(username)
                    await manager.broadcast_typing_users()

                content, _ = word_filter.sanitize(content)

                timestamp = save_message(username, content)
                await manager.broadcast(
                    {
                        "type": "message",
                        "username": username,
                        "content": content,
                        "timestamp": timestamp,
                    }
                )
                continue

            if event_type == "typing":
                is_typing = bool(data.get("isTyping"))
                if is_typing:
                    manager.typing_users.add(username)
                else:
                    manager.typing_users.discard(username)
                await manager.broadcast_typing_users()
                continue

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
