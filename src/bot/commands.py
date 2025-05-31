from aiogram import Router, types, F
from aiogram.types import FSInputFile, CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

import html

from src.bot.keyboards import get_main_menu_button, get_talk_keyboard, get_quiz_action_keyboard
from src.bot.message_sender import send_html_message, send_image_bytes, show_menu
from src.bot.resource_loader import load_message, load_image, load_menu, load_prompt
from src.bot.states import TalkStates, QuizStates
from src.db.repository import GptSessionRepository
from src.db.enums import SessionMode
from services.chatgpt.open_ai_client import OpenAIClient
from settings.config import config

router = Router()

class GptStates(StatesGroup):
    waiting_for_question = State()


@router.message(Command("menu"))
async def back_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    text = await load_message('main')
    image_bytes = await load_image('main')
    menu_commands = await load_menu('main')

    await send_image_bytes(message=message, image_bytes=image_bytes)
    await send_html_message(message=message, text=text)
    await show_menu(bot=message.bot, chat_id=message.chat.id, commands=menu_commands)


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    text = await load_message('main')
    image_bytes = await load_image('main')
    menu_commands = await load_menu('main')

    await send_image_bytes(message=message, image_bytes=image_bytes)
    await send_html_message(message=message, text=text)
    await show_menu(bot=message.bot, chat_id=message.chat.id, commands=menu_commands)


@router.callback_query(F.data == "start")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    text = await load_message('main')
    image_bytes = await load_image('main')
    menu_commands = await load_menu('main')

    await send_image_bytes(message=callback.message, image_bytes=image_bytes)
    await send_html_message(message=callback.message, text=text)
    await show_menu(bot=callback.bot, chat_id=callback.message.chat.id, commands=menu_commands)


@router.message(Command("random"))
async def random(
    message: types.Message,
    state: FSMContext,
    openai_client: OpenAIClient,
    session_repository: GptSessionRepository
):
    user_id = message.from_user.id
    prompt = await load_prompt("random")
    intro = await load_message("random")
    image_bytes = await load_image("random")

    session_id = await session_repository.get_or_create_session(user_id, SessionMode.RANDOM)
    system_prompt = prompt
    user_input = "Give me a random interesting technical fact."

    await session_repository.add_message(session_id, role="user", content=user_input)

    reply = await openai_client.take_task(user_message=user_input, system_prompt=system_prompt)
    await session_repository.add_message(session_id, role="system", content=reply)

    combined = f"{intro}\n\n{reply}"

    await send_image_bytes(message=message, image_bytes=image_bytes)
    await send_html_message(message=message, text=combined)

    await message.answer(
        text="Use the button below to return to the main menu:",
        reply_markup=get_main_menu_button(),
        parse_mode=ParseMode.HTML
    )


@router.message(F.text == "/gpt")
async def gpt_entry(message: types.Message, state: FSMContext):
    text = await load_message("gpt")
    await send_html_message(message, text)
    await state.set_state(GptStates.waiting_for_question)


@router.message(GptStates.waiting_for_question)
async def gpt_reply(
    message: types.Message,
    state: FSMContext,
    openai_client: OpenAIClient,
    session_repository: GptSessionRepository
):
    await send_html_message(message, "⏳ Обробляю запит...")

    user_id = message.from_user.id
    session_id = await session_repository.get_or_create_session(user_id, SessionMode.GPT)

    user_text = message.text.strip()
    await session_repository.add_message(session_id, role="user", content=user_text)

    system_prompt = await load_prompt("gpt")
    reply = await openai_client.take_task(user_message=user_text, system_prompt=system_prompt)
    await session_repository.add_message(session_id, role="system", content=reply)

    await send_html_message(message, reply)


@router.message(F.text == "/talk")
async def talk_to_figure(message: Message, state: FSMContext):
    await state.set_state(TalkStates.figure)
    text = await load_message("talk")
    image_bytes = await load_image("talk")
    persons_list = ['cobain', 'hawking', 'nietzsche', 'queen', 'tolkien']
    persons_text = 'Введіть особистість: ' + ', '.join(persons_list)
    await send_image_bytes(message=message, image_bytes=image_bytes)
    await send_html_message(message=message, text=text)
    await send_html_message(message=message, text=persons_text)


@router.message(TalkStates.figure)
async def set_figure(message: Message, state: FSMContext):
    figure = message.text.strip().lower()
    prompt_path = config.path_to_prompts / f"talk_{figure}.txt"

    if not prompt_path.exists():
        text = await load_message("talk_not_found")
        await message.answer(text)
        return

    prompt = await load_prompt(f"talk_{figure}")
    await state.update_data(system_prompt=prompt, figure=figure)
    await state.set_state(TalkStates.talking)

    image_name = f"talk_{figure}"
    image_bytes = await load_image(image_name)
    
    text = 'Задай своє запитання: '
    await send_image_bytes(message=message, image_bytes=image_bytes)
    await send_html_message(message=message, text=text)


async def send_long_message(message: types.Message, text: str, parse_mode: str = ParseMode.HTML):
    MAX_LENGTH = 4096
    for i in range(0, len(text), MAX_LENGTH):
        chunk = text[i:i + MAX_LENGTH]
        await message.answer(chunk, parse_mode=parse_mode)


@router.message(TalkStates.talking)
async def talk(
    message: Message,
    state: FSMContext,
    openai_client: OpenAIClient,
    session_repository: GptSessionRepository
):
    user_id = message.from_user.id
    user_message = message.text.strip().lower()

    data = await state.get_data()
    system_prompt = data.get("system_prompt")
    figure = data.get("figure")

    session_id = await session_repository.get_or_create_session(user_id, SessionMode.TALK)
    await session_repository.add_message(session_id, role='user', content=user_message)

    gpt_response = await openai_client.take_task(user_message, system_prompt=system_prompt)
    await session_repository.add_message(session_id, role='system', content=gpt_response)

    await send_long_message(message, html.escape(gpt_response), parse_mode=ParseMode.HTML)

    keyboard = await get_talk_keyboard()
    await message.answer(
        text=await load_message("talk_next_action"),
        reply_markup=keyboard
    )


@router.callback_query(F.data == "talk_end")
async def end_talk(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup() 
    await callback.message.answer(await load_message("talk_stop"))
    await callback.answer()


@router.callback_query(F.data == "talk_continue")
async def talk_continue(callback: CallbackQuery):
    await callback.answer("Напишіть наступне повідомлення для продовження розмови.")

