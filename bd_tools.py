import array
import sqlite3
#import mysql
import os
from asyncio import sleep

import aiogram

from handlers.states import texts
from openpyxl.reader.excel import load_workbook
from datetime import datetime, timedelta, time
from openpyxl import Workbook
from calendar import monthrange
from aiogram import types
from aiogram.types import *

from handlers.states import *


users = "users.xlsx"
user = "user"
active = "actual"
services = "haircuts"

class base_activity:

    status = False

async def wait_base():
    import traceback

    k = 0

    while base_activity.status == True and k != 10:
        stack = traceback.extract_stack()
        print('Print from {}'.format(stack[-2][2]))
        await sleep(0.5)
        k+=1
        if k == 10:
            base_activity.status = False
    else:

        return

def bs1():
    import traceback
    stack = traceback.extract_stack()
    print('BS 1 Print from {}'.format(stack[-2][2]))
    base_activity.status = True

def bs2():
    import traceback
    stack = traceback.extract_stack()
    print('BS 2 Print from {}'.format(stack[-2][2]))
    base_activity.status = False

async def validator(u_id):
    await wait_base()  # Предполагается, что это асинхронная функция

    bs1()

    # Подключаемся к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Выполняем запрос для проверки, существует ли пользователь с данным id
    cursor.execute('SELECT status FROM user WHERE id = ?', (u_id,))
    result = cursor.fetchone()  # Получаем результат

    conn.close()  # Закрываем соединение

    bs2()

    if result:
        return result[0]  # Возвращаем статус пользователя
    else:
        return "NoName"  # Если пользователь не найден

async def Create_user(u_id, name, group, tg):

    await wait_base()  # Предполагается, что это асинхронная функция
    bs1()

    group = int(group)

    # Подключаемся к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Вставляем нового пользователя в таблицу 'user'
    cursor.execute('''
    INSERT INTO user (id, name, tg, "group", status, act)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (u_id, name, tg, group, "Student", 0))

    # Сохраняем изменения и закрываем подключение
    conn.commit()
    conn.close()

    bs2()  # Вызываем функцию для выполнения последующих действий

async def main_menu_text(u_id):
    await wait_base()  # Предполагается, что это асинхронная функция

    bs1()

    # Подключаемся к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверяем, есть ли активные записи для данного пользователя
    cursor.execute('SELECT COUNT(*) FROM user WHERE id = ? AND act = 0', (u_id,))
    has_active_records = cursor.fetchone()[0] == 0

    cursor.execute('SELECT "group" FROM user WHERE id = ?', (u_id,))
    f = cursor.fetchone()
    group = f[0]

    if not has_active_records:
        conn.close()  # Закрываем соединение
        bs2()
        return "Похоже, сейчас у вас нет активных записей!"

    # Получаем активные записи для данного пользователя
    cursor.execute(f'SELECT row_number FROM actual_orders_{group} WHERE id = ?', (u_id,))
    records = cursor.fetchall()  # Получаем все активные записи

    conn.close()  # Закрываем соединение
    # Форматируем вывод
    if not records:
        bs2()
        return "Похоже, сейчас у вас нет активных записей!"

    returning_array = ""

    returning_array += (
        f"----------------\n"
        f"Ваши места:\n"
    )


    for record in records:
        returning_array += f"Место - {record[0]}\n"

    returning_array += "----------------"

    bs2()
    return returning_array

async def create_order(u_id, link):

    await wait_base()  # Предполагается, что это асинхронная функция
    bs1()

    # Подключаемся к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Проверяем значение 'act' пользователя
    cursor.execute('SELECT act FROM user WHERE id = ? ', (u_id,))
    check = cursor.fetchone()

    if check == 6:
        conn.close()
        bs2()
        return False

    # Получаем информацию о пользователе
    cursor.execute('SELECT name, "group", tg FROM user WHERE id = ?', (u_id,))
    res = cursor.fetchone()
    name = res[0]
    group = res[1]
    tg = res[2]

    # Получаем текущее количество записей для пересчета row_number
    cursor.execute(f"SELECT COUNT(*) FROM actual_orders_{group}")
    count = cursor.fetchone()[0]
    new_row_number = count + 1

    # Вставляем новую запись с row_number
    cursor.execute(f'''
    INSERT INTO actual_orders_{group} (id, name, tg, link, ord_id, row_number)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (u_id, name, tg, link, new_row_number, new_row_number))

    # Обновляем поле 'act' у пользователя
    cursor.execute("UPDATE user SET act = act + 1 WHERE id = ?", (u_id,))

    # Сохраняем изменения и закрываем подключение
    conn.commit()
    conn.close()

    bs2()  # Вызываем функцию для выполнения последующих действий

    return True

async def change_role(u_id):

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE user SET status = ? WHERE id = ?", ("Teacher", u_id)
    )

    conn.commit()
    conn.close()

async def teacher_main_menu_text():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM actual_orders_1")

    one = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM actual_orders_2")

    two = cursor.fetchone()[0]

    conn.close()

    ret = (f"Записей в первой подргуппе - {one}\n"
           f"Записей во второй подргуппе - {two}\n"
           f"Выберите, из какой подгруппы выбрать запись:")

    return ret

def reset_row_numbers(database_path, table_name):
    """Сбрасываем номера строк, чтобы избежать уникальных конфликтов."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Устанавливаем row_number в NULL, чтобы обнулить уникальные значения
    query = f"UPDATE {table_name} SET row_number = 0"
    cursor.execute(query)
    conn.commit()
    conn.close()

def get_recalculated_row_numbers(database_path, table_name):
    """Пересчитываем и обновляем номера строк в поле row_number."""
    reset_row_numbers(database_path, table_name)  # Сначала сбрасываем row_number

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Получаем все строки и сортируем по ord_id, чтобы каждая строка была уникальной
    query = f"SELECT ord_id FROM {table_name} ORDER BY ord_id"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Обновляем поле row_number для каждой строки
    for idx, (ord_id,) in enumerate(rows, start=1):
        update_query = f"UPDATE {table_name} SET row_number = ? WHERE ord_id = ?"
        cursor.execute(update_query, (idx, ord_id))

    conn.commit()
    conn.close()

async def show_order_info(group):
    # Подключаемся к базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute( f"SELECT * FROM actual_orders_{group} ORDER BY rowid LIMIT 1")

    id, name, link, ord_id, tg, row_num = cursor.fetchone()

    conn.close()

    print(row_num,  "- ROW NUM")

    return id, name, link, row_num, tg

async def get_order_info(id, name, link, ord_id, tg):

     ret = (
         f"Имя - {name}\n"
         f"TG - {tg}\n"
         f"Ссылка - {link}"
     )

     return ret

async def end_order(id, name, link, ord_id, tg, group):
    print(ord_id, ' ', group, ' ', " - END")


    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM actual_orders_{group} WHERE row_number = {ord_id}")

    cursor.execute("UPDATE user SET act = act - 1 WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    get_recalculated_row_numbers("users.db", f"actual_orders_{group}")

async def get_order_to_delete(u_id):

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT "group" FROM user WHERE id = ? ', (u_id,))
    group = cursor.fetchone()[0]

    query = "SELECT * FROM actual_orders_" + str(group) + " WHERE id = ?"
    cursor.execute(query, (u_id,))

    # Получаем все результаты
    records = cursor.fetchall()

    records.insert(0, group)

    conn.close()

    return records

async def text_to_delete(array):
    print(array, " - TEXT")


    if array != [1]:
        """[(938952509, 'Валера', '3', 3, 'vabbaj', 1)]"""

        ret = "Вот ваши записи:\n"
        for i in range(1, len(array)):
            ret += str(i) + " - " + array[i][2] + "\n"

        ret+= "Нажмите на кнопку с цифрой для мгновенного удаления записи, или же Назад, если передумали"

        return ret

    else:

        return "У вас нет активных записей!"












































