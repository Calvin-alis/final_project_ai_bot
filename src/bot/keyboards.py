from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from src.bot.resource_loader import load_message


def get_main_menu_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🏘️ Main Menu', callback_data='start')]
        ]
    )


async def get_talk_keyboard() -> ReplyKeyboardMarkup:
    continue_btn = KeyboardButton(text=await load_message("talk_continue"))
    stop_btn = KeyboardButton(text=await load_message("talk_stop"))

    return ReplyKeyboardMarkup(
        keyboard=[
            [continue_btn],
            [stop_btn]
        ],
        resize_keyboard=True
    )


def get_quiz_action_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Ще одне питання")],
            [KeyboardButton(text="📚 Змінити тему")],
            [KeyboardButton(text="⛔️ Завершити квіз")]
        ],
        resize_keyboard=True
    )