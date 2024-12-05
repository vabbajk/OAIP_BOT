from datetime import datetime
import sqlite3

from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from aiogram import Bot, Dispatcher, types

from bot_box import bot
from handlers import start, default


def cr():
    # Создаем подключение к базе данных (если файла нет, он будет создан)
    conn = sqlite3.connect('users.db')

    # Создаем курсор для выполнения SQL-команд
    cursor = conn.cursor()

    # Создаем таблицу для пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        inst TEXT,
        tg TEXT,
        status TEXT,
        ban_status TEXT,
        actual_orders INTEGER,
        past_orders INTEGER
    )
    ''')

    # Создаем таблицу для актуальных заказов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS actual_orders (
        id INTEGER KEY,
        name TEXT,
        phone TEXT,
        inst TEXT,
        tg TEXT,
        master_id INTEGER,
        date TEXT,
        time INTEGER,
        long INTEGER,
        [order] TEXT,
        cost INTEGER,
        comment TEXT
    )
    ''')

    # Создаем таблицу для прошлых заказов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS past_orders (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        inst TEXT,
        tg TEXT,
        master_id INTEGER,
        date TEXT,
        time INTEGER,
        long INTEGER,
        [order] TEXT,
        cost INTEGER,
        comment TEXT
    )
    ''')
    # Сохраняем изменения и закрываем подключение
    conn.commit()
    conn.close()






storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_routers(start.router, default.router)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())