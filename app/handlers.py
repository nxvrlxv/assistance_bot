from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.gpt_response as gr
from app.db import add_reminder
from app.db import get_reminders
import asyncio
from datetime import datetime

import app.keyboards as kb

OPENAI_API_KEY = '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'


router = Router()

class Prompt(StatesGroup):
    text_prompt = State()
    image_prompt = State()

class Rmndrs(StatesGroup):
    text_of_reminder = State()
    time_of_reminder = State()





@router.message(CommandStart())
async def privet(message: Message):
    await message.answer('Привет, что хочешь узнать?', reply_markup=kb.main)



@router.message(Command('help'))
async def helping(message: Message):
    await message.answer('Вот все доступные команды')


@router.callback_query(F.data == 'generate')
async def generate(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Пиши сюда свой вопрос, а я на него отвечу)')
    await state.set_state(Prompt.text_prompt)


@router.message(Prompt.text_prompt)
async def zapros(message: Message, state: FSMContext):
    await message.reply('Сейчас отвечу бро')
    mess = message.text
    gpt_response = await asyncio.get_event_loop().run_in_executor(None, gr.get_response, message.from_user.id, mess)
    await message.reply(gpt_response, reply_markup=kb.exit_kb)



@router.callback_query(F.data == 'image')
async def image_response(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Пиши промпт')
    await state.set_state(Prompt.image_prompt)


@router.message(Prompt.image_prompt)
async def get_image(message: Message):
    await message.reply('Генерирую картинку, подождите')
    mess = message.text
    image = await asyncio.get_event_loop().run_in_executor(None, gr.get_image, mess)
    await message.answer(image, reply_markup=kb.exit_kb)


@router.callback_query(F.data == 'exit')
async def exit_(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer('Снова тут?', reply_markup=kb.main)



@router.message(Command('get_id'))
async def id_(message: Message):
    idi = message.from_user.id
    await message.reply(f'Вот твой id: {idi}')


@router.message(Command('history'))
async def history(message: Message):
    await message.answer(f'Вот история вашего общения: {gr.user_contexts}')


@router.message(Command('clear_history'))
async def clear_history(message: Message):
    gr.user_contexts[message.from_user.id] = []
    await message.answer('История очищена')

remind = {}
@router.callback_query(F.data == 'reminder')
async def add_reminders(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Rmndrs.text_of_reminder)
    remind[callback.from_user.id] = {}
    await callback.message.answer('Введите текст напоминания')

@router.message(Rmndrs.text_of_reminder)
async def rmndr_text(message: Message, state: FSMContext):
    mess = message.text
    remind[message.from_user.id]['text'] = mess
    await message.answer('Введите время в формате: часы:минуты день.месяц.год')
    await state.set_state(Rmndrs.time_of_reminder)

@router.message(Rmndrs.time_of_reminder)
async def rmndr_time(message: Message, state: FSMContext):
    text = message.text
    time = datetime.strptime(text, "%H:%M %d.%m.%Y").isoformat()
    remind[message.from_user.id]['time'] = time
    await state.clear()
    await asyncio.get_event_loop().run_in_executor(None, add_reminder, message.from_user.id, remind[message.from_user.id]['time'], remind[message.from_user.id]['text'])
    await message.answer('напоминание сохранено')


@router.callback_query(F.data == 'today_reminders')
async def list_of_reminders(callback: CallbackQuery):
    await callback.answer()

    all_reminders = await asyncio.get_event_loop().run_in_executor(None, get_reminders, callback.from_user.id)

    formatted_reminders = []
    for reminder in all_reminders:
        text, status, time_of_reminder = reminder
        dt = datetime.fromisoformat(time_of_reminder)
        time_of_reminder = dt.strftime('%H:%M')
        formatted_reminders.append(f'{text} {time_of_reminder}')

    if formatted_reminders:
        response = "Ваши напоминания:\n" + "\n".join(formatted_reminders)
    else:
        response = "У вас нет активных напоминаний."

    await callback.message.answer(response)


