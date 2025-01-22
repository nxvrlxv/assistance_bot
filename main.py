import asyncio
import logging
from app.db import init_db
from app.db import check_reminders


from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router


bot = Bot(token=TOKEN)
dp = Dispatcher() # задача обрабатывать апдейты

async def on_start_up():
    asyncio.create_task(check_reminders(bot))

async def main():
    init_db()
    dp.include_router(router)
    await bot.send_message(chat_id=1947097070, text='Люблю тебя, малыш')
    await bot.send_message(chat_id=923885757, text='Эй, как ты?')
    await bot.send_message(chat_id=817798475, text='Эй, как ты?')
    asyncio.create_task(on_start_up())
    await dp.start_polling(bot) # .start_polling() отправляет запрос на серваки тг, если ответ есть, то наш бот его отработает, иначе ожидание ответа



if __name__ == '__main__':    # данная конструкция позволяет запускать эту функцию только в том случае, если мы запускаем именно этот файл, а не импортируем
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())  # запуск асинхронной функции
    except KeyboardInterrupt:
        print('все гг боту')