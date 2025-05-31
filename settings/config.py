# pip install pydantic-settings
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class AppConfig(BaseSettings):
    openai_api_token : str 
    telegram_bot_api_key: str 
    
    opeanai_model: str = 'gpt-3.5-turbo'
    opeanai_model_temperature: float = 0.75 # 0 - 2.0
    
    username: str | None = None
    password: str | None = None
    
    path_to_messages: Path = BASE_DIR / 'resources' / 'messages'
    path_to_images: Path = BASE_DIR / 'resources' / 'images'
    path_to_menus:  Path = BASE_DIR / 'resources' / 'menus'
    path_to_prompts:  Path = BASE_DIR / 'resources' / 'prompts'
    
    path_to_logs: Path = BASE_DIR / 'logs'
    
    path_to_db: Path = BASE_DIR / 'storage' / 'chat_sessions.db'
    
    model_config = SettingsConfigDict(
        env_file = str(BASE_DIR / '.env'), 
        env_file_encoding = 'utf-8'
    )
    
config = AppConfig()
