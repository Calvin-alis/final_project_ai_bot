import sqlite3
from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from settings.config import config


class DatabaseInitializer:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def create_tables(self) -> None:
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            QUERY_CREATE_TABLE = '''
                CREATE TABLE IF NOT EXISTS gpt_sessions (
                    id INTEGER PRIMARY KEY
                    , tg_user_id INTEGER NOT NULL
                    , mode TEXT NOT NULL
                    , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    , UNIQUE(tg_user_id, mode)
                );
            '''
            
            QUERY_MESSAGES = '''
                CREATE TABLE IF NOT EXISTS gpt_messages (
                    id INTEGER PRIMARY KEY
                    , session_id INTEGER NOT NULL
                    , role TEXT NOT NULL CHECK(role IN ('user', 'system'))
                    , content TEXT NOT NULL
                    , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    , FOREIGN KEY(session_id) REFERENCES gpt_sessions(id) ON DELETE CASCADE
                );
            '''
            cursor.execute(
                QUERY_CREATE_TABLE
            )
            
            cursor.execute(
                QUERY_MESSAGES
            )
            
            conn.commit()
