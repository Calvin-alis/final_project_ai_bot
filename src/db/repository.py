from pathlib import Path

# CRUD - create, read, update ( insert ), delete
class GptSessionRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        
    async def get_or_create_session(self, tg_user_id: int, mode: str) -> int:
        pass
    
    
    async def add_message(self, session_id:int, role: str, content: str) -> None:
        pass
    
    
    async def get_messages(self, session_id: int) -> list[dict]:
        pass
    
    
    async def clear_session(self, session_id: int) -> None:
        pass
        