from aiogram import Router, Bot
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from keyboards import *
from bd_tools import validator, Create_user, main_menu_text, teacher_main_menu_text
from handlers.states import registration, default, Teacher
from bot_box import bot
router = Router()


async def admin_main_menu_text(u_id):
    pass


@router.message(Command("start"))
async def starting(message: types.Message, state: FSMContext):

    u_id = message.from_user.id
    await state.update_data(u_id = u_id)

    match await validator(u_id):
        case "NoName":
            await state.set_state(registration.reg_name)
            await bot.send_message(u_id, text="Здравствуйте, как вас зовут?")
            return
        case "Student":
            markup = await default_user_markup()
            await state.set_state(default.default)
            await bot.send_message(u_id, text=await main_menu_text(u_id), reply_markup=markup)
        case "Teacher":

            markup = await default_admin_markup()
            await state.set_state(Teacher.default)
            await bot.send_message(u_id, text=await teacher_main_menu_text(), reply_markup=markup)

@router.message(StateFilter(None))
async def start(message: types.Message, state: FSMContext):
    if message.text:
        u_id = message.from_user.id
        await state.update_data(u_id=u_id)

        match await validator(u_id):
            case "NoName":
                await state.set_state(registration.reg_name)
                await bot.send_message(u_id, text="Здравствуйте, как вас зовут?")
                return
            case "Client":
                markup = await default_user_markup()
                await bot.send_message(u_id, text=await main_menu_text(u_id), reply_markup=markup)

@router.callback_query(StateFilter(None))
async def start(callback: types.CallbackQuery, state: FSMContext):
    u_id = callback.from_user.id
    await state.update_data(u_id=u_id)

    match await validator(u_id):
        case "NoName":
            await state.set_state(registration.reg_name)
            await bot.send_message(u_id, text="Здравствуйте, как вас зовут?")
            return
        case "Student":
            markup = await default_user_markup()
            await state.set_state(default.default)
            await bot.send_message(u_id, text=await main_menu_text(u_id), reply_markup=markup)
        case "Teacher":

            markup = await default_admin_markup()
            await state.set_state(Teacher.default)
            await bot.send_message(u_id, text=await teacher_main_menu_text(), reply_markup=markup)

@router.message(StateFilter(registration.reg_name))
async def start(message: types.Message, state: FSMContext):

    if message.text:

        await state.update_data(u_id = message.chat.id, name = message.text, username = message.from_user.username)
        u_id = message.from_user.id

        await bot.send_message(u_id, text="В какой вы подргуппе (1 или 2)?", reply_markup= await one_or_two())

        await state.set_state(registration.reg_group)

@router.callback_query(StateFilter(registration.reg_group))
async def start(callback: types.CallbackQuery, state: FSMContext):
    u_data = await state.get_data()
    u_id = u_data.get("u_id")
    name = u_data.get("name")
    username = u_data.get("username")

    await bot.send_message(u_id, text="Спасибо за регистрацию! Нажмите кнопку 'Новая запись' для создания новой записи (до 6 одновременно), или же кнопку 'Mои записи', чтобы посмотреть свои записи",
                           reply_markup= await default_user_markup())

    await Create_user(u_id, name, callback.data, username)

    await state.set_state(default.default)
