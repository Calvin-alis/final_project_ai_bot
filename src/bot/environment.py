
from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import TelegramObject

class EnvironmentMiddleware(BaseMiddleware):
    def __init__(self, **kwargs):
        self.data = kwargs

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data.update(self.data)
        return await handler(event, data)
