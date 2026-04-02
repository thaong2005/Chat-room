from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

DB_PATH = Path(__file__).resolve().parents[1] / "chat.db"


class Message(TypedDict):
    username: str
    content: str
    timestamp: str


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_message(username: str, content: str) -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO messages (username, content, created_at) VALUES (?, ?, ?)",
            (username, content, timestamp),
        )
        conn.commit()
    return timestamp


def get_recent_messages(limit: int = 100) -> list[Message]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT username, content, created_at
            FROM (
                SELECT username, content, created_at
                FROM messages
                ORDER BY id DESC
                LIMIT ?
            ) recent
            ORDER BY created_at ASC
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "username": row[0],
            "content": row[1],
            "timestamp": row[2],
        }
        for row in rows
    ]
