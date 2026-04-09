# Chatroom MVP (Python)

A local-first chatroom MVP inspired by Discord/Messenger flows, focused on one room with:
- live messages (WebSocket)
- online user list
- typing indicator
- message history persistence (SQLite)

## Stack
- Backend: FastAPI + WebSockets
- Database: SQLite
- Frontend: lightweight static web app served by FastAPI

## Run locally
1. Open terminal in project root.
2. Create virtual environment:
   - Windows PowerShell: `python -m venv .venv`
3. Activate it:
   - `./.venv/Scripts/Activate.ps1`
4. Install dependencies:
   - `pip install -r backend/requirements.txt`
5. Start server:
   - `uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000`
6. Open browser:
   - `http://127.0.0.1:8000`

## Notes
- Messages are persisted in `backend/chat.db`.
- Max message length is 500 characters.
- Simple bad-word filter is enabled with ANTLR grammar (`backend/app/filter/ChatMessage.g4`).
- Default bad words are in `backend/app/filter/bad_words.txt` (one word per line).
- Messages containing invalid words are masked before saving and broadcasting.
- Open two browser tabs/windows to test real-time room behavior.

## Regenerate ANTLR parser/lexer
If you update the grammar, regenerate Python files with:

```powershell
java -jar "C:/antlr/antlr4-4.9.2-complete.jar" -Dlanguage=Python3 -o "backend/app/filter/generated" "backend/app/filter/ChatMessage.g4"
```

Or use the helper script:

```powershell
python backend/run.py gen
python backend/run.py test
```

## Next upgrade ideas
- Multi-room support with room code join/create
- Proper auth (email/password or OAuth)
- PostgreSQL + Alembic migrations
- Redis pub/sub if scaling to multiple backend instances
