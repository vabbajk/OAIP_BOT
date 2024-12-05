from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

class registration(StatesGroup):
    reg_name = State()
    reg_group = State()

class default(StatesGroup):
    default = State()
    send_link = State()
    confirm = State()

    chose_my = State()
    action_my = State()
    redact_my = State()
    delete_my = State()

class Teacher(StatesGroup):

    default = State()
    call = State()





class texts:
    no_time = "Свободного времени нет"
    new_order = "Новая запись"
    look = "Мои записи"
    today_orders = "Сегодня"
    all_orders = "Все записи"
    one = "1"
    two = "2"
    back = "Назад"
    end = "Завершить"
    delete = "Удалить"
    skip = "Пропустить"




