import sqlite3
from pathlib import Path
from typing import Optional

class GptSessionRepository:
    def __init__(self, db_path: str):
        self.db_path = str(db_path) 

    async def get_or_create_session(self, tg_user_id: int, mode: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
           
            cursor.execute(
                "SELECT id FROM gpt_sessions WHERE tg_user_id = ? AND mode = ?",
                (tg_user_id, mode)
            )
            result = cursor.fetchone()
            if result:
                return result[0]

            cursor.execute(
                "INSERT INTO gpt_sessions (tg_user_id, mode) VALUES (?, ?)",
                (tg_user_id, mode)
            )
            conn.commit()
            return cursor.lastrowid

    async def add_message(self, session_id: int, role: str, content: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gpt_messages (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )
            conn.commit()

    async def get_messages(self, session_id: int) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM gpt_messages WHERE session_id = ? ORDER BY created_at ASC",
                (session_id,)
            )
            rows = cursor.fetchall()
            return [{"role": role, "content": content} for role, content in rows]

    async def clear_session(self, session_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM gpt_messages WHERE session_id = ?",
                (session_id,)
            )
            conn.commit()
