from aiogram import Router, Bot
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

import bot_box
from handlers.start import default_admin_markup
from keyboards import *
from bd_tools import validator, Create_user, main_menu_text, create_order, change_role, teacher_main_menu_text, \
    show_order_info, get_order_info, end_order, get_order_to_delete, text_to_delete
from handlers.states import registration, default, Teacher
from bot_box import bot
router = Router()


@router.callback_query(StateFilter(default.default))
async def start(callback: types.CallbackQuery, state: FSMContext):
    u_data = await state.get_data()
    u_id = u_data.get("u_id")

    match callback.data:

        case texts.new_order:

            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text="Пришлите мне ссылку на ваш отчет:",
                                        reply_markup=await back_button())

            await state.set_state(default.send_link)

        case texts.delete:

            await state.set_state(default.delete_my)

            array = await get_order_to_delete(u_id)

            await state.update_data(array = array)

            await bot.edit_message_text(chat_id = callback.message.chat.id,
                                        message_id= callback.message.message_id, text=await text_to_delete(array), reply_markup=await delete_markup(array))

@router.callback_query(StateFilter(default.delete_my))
async def start(callback: types.CallbackQuery, state: FSMContext):
    u_data = await state.get_data()
    u_id = u_data.get("u_id")

    if callback.data == texts.back:
        markup = await default_user_markup()
        await state.set_state(default.default)
        await bot.edit_message_text(chat_id=u_id,
                                    message_id=callback.message.message_id,text=await main_menu_text(u_id), reply_markup=markup)

        return

    array = u_data.get("array")
    print(array[int(callback.data)], ' KKKK')
    """[(938952509, 'Валера', '3', 3, 'vabbaj', 1)]"""
    await end_order(array[int(callback.data)][0],
                    array[int(callback.data)][1],
                    array[int(callback.data)][2],
                    array[int(callback.data)][5],
                    array[int(callback.data)][4],
                    array[0],
                    )

    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=await main_menu_text(u_id),
                                reply_markup=await default_user_markup())

    await state.set_state(default.default)

@router.message(StateFilter(default.default))
async def start(message: types.Message, state: FSMContext):

    if message.text == bot_box.password:

        await change_role(message.chat.id)

        markup = await default_admin_markup()
        await state.set_state(Teacher.default)
        await bot.send_message(message.chat.id, text=await teacher_main_menu_text(), reply_markup=markup)

@router.message(StateFilter(default.send_link))
async def start(message: types.Message, state: FSMContext):

    if message.text:

        u_data = await state.get_data()
        u_id = u_data.get("u_id")

        a = await create_order(u_id, message.text)

        if(a):

            await bot.send_message(u_id,
                                   text="Ваша запись успешно создана!")

            await bot.send_message(u_id,
                                   text=await main_menu_text(u_id),
                                   reply_markup=await default_user_markup())

            await state.set_state(default.default)

        else:

            await bot.send_message(u_id,
                                   text="Произошла ошибка записи! Возможно, вы уже записались максимальное количество раз(")

            await bot.send_message(u_id,
                                   text=await main_menu_text(u_id),
                                   reply_markup=await default_user_markup())

            await state.set_state(default.default)

@router.callback_query(StateFilter(default.send_link))
async def start(callback: types.CallbackQuery, state: FSMContext):

    u_id = callback.message.chat.id

    if callback.data == texts.back:

        markup = await default_user_markup()
        await state.set_state(default.default)
        await bot.send_message(u_id, text=await main_menu_text(u_id), reply_markup=markup)

        return

    markup = await default_user_markup()
    await state.set_state(default.default)
    await bot.send_message(callback.message.chat.id, text=await main_menu_text(callback.message.chat.id), reply_markup=markup)

@router.callback_query(StateFilter(Teacher.default))
async def start(callback: types.CallbackQuery, state: FSMContext):
    u_data = await state.get_data()
    u_id = u_data.get("u_id")

    match callback.data:

        case texts.one:

            id, name, link, ord_id, tg = await show_order_info(1)

            await state.update_data(id = id, name = name, link = link, tg = tg, ord_id = ord_id, group = 1)

            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=await get_order_info(id, name, link, ord_id, tg),
                                        reply_markup=await action())

            await state.set_state(Teacher.call)

        case texts.two:

            id, name, link, ord_id, tg = await show_order_info(2)

            await state.update_data(id=id, name=name, link=link, tg=tg, ord_id=ord_id, group = 2)

            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=await get_order_info(id, name, link, ord_id, tg),
                                        reply_markup=await action())

            await state.set_state(Teacher.call)

@router.callback_query(StateFilter(Teacher.call))
async def start(callback: types.CallbackQuery, state: FSMContext):
    u_data = await state.get_data()
    u_id = u_data.get("u_id")

    match callback.data:

        case texts.end:

            id = u_data.get("id")
            name = u_data.get("name")
            link = u_data.get("link")
            ord_id = u_data.get("ord_id")
            tg = u_data.get("tg")
            group = u_data.get("group")
            #print(ord_id)

            await end_order(id, name, link, ord_id, tg, group)

            markup = await default_admin_markup()

            await state.set_state(Teacher.default)

            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text= await teacher_main_menu_text(),
                                        reply_markup=markup)

        case texts.back:

            markup = await default_admin_markup()
            await state.set_state(Teacher.default)
            await bot.send_message(u_id, text=await teacher_main_menu_text(), reply_markup=markup)





