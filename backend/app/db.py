from __future__ import annotations

import sqlite3
import hashlib
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
                created_at TEXT NOT NULL,
                isFlagged BOOL DEFAULT FALSE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                faults INTEGER NOT NULL DEFAULT 0
            )            
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_name TEXT NOT NULL,
                password TEXT NOT NULL
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

# hash password func
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            hashed_password = hash_password(password)
            conn.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False # user alr exists

def verify_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        hashed_password = hash_password(password)
        cursor = conn.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, hashed_password))
        return cursor.fetchone() is not None