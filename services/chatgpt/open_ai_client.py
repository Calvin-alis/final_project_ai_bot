
from settings import get_logger
from openai import AsyncOpenAI, OpenAIError

logger = get_logger(__name__)

class OpenAIClient:
    
    def __init__(self, openai_api_key: str, model:str, temperature: float):
        self._client = AsyncOpenAI(api_key = openai_api_key)
        self._model = model
        self._temperature = temperature
    
    
    async def take_task(self, user_message: str, system_promt: str = 'You assistant') -> str | None:
        try:
            response = await self._client.chat.completions.create(
                model = self._model
                , messages = [
                    {'role': 'system', 'content': system_promt}, 
                    {'role': 'user', 'content': user_message}
                ],
                temperature= self._temperature
            )
            
            return response.choices[0].message.content 
        except OpenAIError as e:
            logger.error(f'OpenAI Error: {e}')
            raise
       