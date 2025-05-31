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


async def get_talk_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Продовжити", callback_data="talk_continue")],
        [InlineKeyboardButton(text="🚫 Завершити розмову", callback_data="talk_end")]
    ])
    return keyboard


def get_quiz_action_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔁 Ще одне питання")],
            [KeyboardButton(text="📚 Змінити тему")],
            [KeyboardButton(text="⛔️ Завершити квіз")]
        ],
        resize_keyboard=True
    )