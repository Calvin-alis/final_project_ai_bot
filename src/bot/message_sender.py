from aiogram import types
from aiogram.types import BufferedInputFile
from aiogram.types import InputFile, BotCommand, BotCommandScopeChat, MenuButtonCommands


async def send_html_message(message: types.Message, text: str) -> None:
    await message.answer(text=text, parse_mode='HTML')


async def send_image_bytes(
    message: types.Message,
    image_bytes: bytes,
    image_name: str = 'image.jpg',
    caption: str | None = None,
    parse_mode: str = 'HTML'
) -> None:
    await message.answer_photo(
        photo=BufferedInputFile(image_bytes, filename=image_name),
        caption=caption,
        parse_mode=parse_mode
    )
    
    
async def show_menu(bot, chat_id: int, commands: dict[str, str]) -> None:
    command_list = [BotCommand(command=cmd, description=desc) for cmd, desc in commands.items()]
    await bot.set_my_commands(command_list, scope=BotCommandScopeChat(chat_id=chat_id))
    await bot.set_chat_menu_button(chat_id=chat_id, menu_button=MenuButtonCommands())
