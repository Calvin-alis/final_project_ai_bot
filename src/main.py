
from db.initializator import DatabaseInitializer
from db.repository import GptSessionRepository

from services.chatgpt.open_ai_client import OpenAIClient
from settings.config import config 

# D100, D103, 
def main():
    db_initializator = DatabaseInitializer(config.path_to_db)
    db_initializator.create_tables()
    
    session_repository = GptSessionRepository(config.path_to_db)
    
    opeanai_client = OpenAIClient(
        openai_api_key = config.openai_api_token,
        model = config.opeanai_model,
        temperature= config.opeanai_model_temperature
    )
    
    # bot config 
    

if __name__ == '__main__':
    main()
    