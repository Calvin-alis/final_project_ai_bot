import asyncio
import sys

from settings.config import config

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    
    
# @dp.message_handler(commands=['help']) # /help
# async def send_welcome(message: types.Message):
#     await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


async def main() -> None:
    bot = Bot(token=config)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())