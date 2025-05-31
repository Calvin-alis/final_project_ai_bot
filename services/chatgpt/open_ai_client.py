from settings.logging_config import get_logger
from openai import AsyncOpenAI, OpenAIError

logger = get_logger(__name__)

class OpenAIClient:
    
    def __init__(self, openai_api_key: str, model: str, temperature: float):
        self._client = AsyncOpenAI(api_key=openai_api_key)
        self._model = model
        self._temperature = temperature
    
    async def take_task(self, user_message: str, system_prompt: str) -> str:
        try:
            logger.info(f"[GPT REQUEST] SYSTEM PROMPT:\n{system_prompt}")
            logger.info(f"[GPT REQUEST] USER MESSAGE:\n{user_message}")
            
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_message}
                ],
                temperature=self._temperature
            )
            
            reply = response.choices[0].message.content
            logger.info(f"[GPT RESPONSE]\n{reply}")
            return reply

        except OpenAIError as e:
            logger.error(f'[GPT ERROR] {e}')
            return "⚠️ Виникла помилка при зверненні до GPT. Спробуйте ще раз."
