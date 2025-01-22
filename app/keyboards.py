from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup ,InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сгенерировать', callback_data='generate')],
    [InlineKeyboardButton(text='Картинка', callback_data='image')],
    [InlineKeyboardButton(text='напоминание', callback_data='reminder')],
    [InlineKeyboardButton(text='Напоминания на сегодня', callback_data='today_reminders')]
])

exit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='выход', callback_data='exit')]
])

