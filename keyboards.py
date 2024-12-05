from calendar import monthrange
import calendar

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from handlers.states import texts
from datetime import *


async def default_user_markup():

    b1 = InlineKeyboardButton(text=texts.new_order, callback_data=texts.new_order)
    b2 = InlineKeyboardButton(text=texts.delete, callback_data=texts.delete)

    r1 = [b1, b2]

    keyboard = [r1]

    rpl = InlineKeyboardMarkup(inline_keyboard=keyboard, one_time_keyboard=False, row_width=1)

    return rpl

async def one_or_two():

    b1 = InlineKeyboardButton(text=texts.one, callback_data=texts.one)
    b2 = InlineKeyboardButton(text=texts.two, callback_data=texts.two)

    r1 = [b1, b2]

    keyboard = [r1]

    rpl = InlineKeyboardMarkup(inline_keyboard=keyboard, one_time_keyboard=False, row_width=1)

    return rpl

async def back_button():

    b1 = InlineKeyboardButton(text=texts.back, callback_data=texts.back)

    r1 = [b1]

    keyboard = [r1]

    rpl = InlineKeyboardMarkup(inline_keyboard=keyboard, one_time_keyboard=False, row_width=1)

    return rpl

async def default_admin_markup():

    b1 = InlineKeyboardButton(text=texts.one, callback_data=texts.one)
    b2 = InlineKeyboardButton(text=texts.two, callback_data=texts.two)

    r1 = [b1, b2]

    keyboard = [r1]

    rpl = InlineKeyboardMarkup(inline_keyboard=keyboard, one_time_keyboard=False, row_width=1)

    return rpl

async def action():

    b1 = InlineKeyboardButton(text=texts.back, callback_data=texts.back)
    b2 = InlineKeyboardButton(text=texts.end, callback_data=texts.end)

    r1 = [b1, b2]

    keyboard = [r1]

    rpl = InlineKeyboardMarkup(inline_keyboard=keyboard, one_time_keyboard=False, row_width=1)

    return rpl

async def delete_markup(array):

    if array != [1]:

        print(array , " - KEYBOARDS")

        r = []
        keyboard = []

        for i in range(1, len(array)):

            r.append(InlineKeyboardButton(text=str(i), callback_data=str(i)))

            if(len(r) == 4):

                keyboard.append(r)

                r = []

        if len(r) != 0:

            keyboard.append(r)

        r = []

        r.append(InlineKeyboardButton(text=texts.back, callback_data=texts.back))
        keyboard.append(r)

        rpl = InlineKeyboardMarkup(inline_keyboard=keyboard, one_time_keyboard=False, row_width=1)

        return rpl

    else:
        keyboard = []

        r = [InlineKeyboardButton(text=texts.back, callback_data=texts.back)]

        keyboard.append(r)

        rpl = InlineKeyboardMarkup(inline_keyboard=keyboard, one_time_keyboard=False, row_width=1)

        return rpl