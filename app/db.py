import sqlite3
import asyncio
from datetime import datetime


def init_db():
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            reminder_time TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'active'
        )
    ''')

    conn.commit()
    conn.close()


def add_reminder(user_id: int, reminder_time, message: str):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute('''
           INSERT INTO reminders (user_id, reminder_time, message)
           VALUES (?, ?, ?)
       ''', (user_id, reminder_time, message))
    conn.commit()
    conn.close()

async def check_reminders(bot):
    while True:
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()

        now = datetime.now().isoformat(timespec='seconds')
        reminders = cursor.execute('''SELECT id, user_id, message FROM reminders
        WHERE reminder_time <= ? and status = 'active' ''', (now,)).fetchall()

        for reminder in reminders:
            reminder_id, user_id, message = reminder

            try:
                 await bot.send_message(user_id, f'Напоминаю: {message}')

            except sqlite3.Error:
                print('ошибка в работе с бд')

            cursor.execute(''' 
            UPDATE reminders
            SET status = 'sent' 
            WHERE id = ?''', (reminder_id,))

        conn.commit()
        conn.close()

        await asyncio.sleep(60)


def get_reminders(user_id: int):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d")

    cursor.execute('''select message, status, reminder_time from reminders
    where user_id = ? and reminder_time like ?''', (user_id, f'{now}%'))

    all_reminders = cursor.fetchall()
    conn.commit()
    conn.close()
    return all_reminders



