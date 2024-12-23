import time

from aiogram import F, types, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

import kb
import text
import db
import config

dp = Dispatcher()

db_process = db.options_db()

@dp.message(Command(config.commands[0][1:])) #/start
async def start_handler(msg: Message):
    text_msg = db_process.add_user(msg.from_user.id, msg.chat.username, config.statuses[0], text.start_text[2])
    await msg.answer(text_msg[1], reply_markup=kb.start)

@dp.message()
async def add(msg: Message): #действия
    text_msg = text.start_text[1]

    if db_process.check_status(msg.from_user.id, config.statuses[2]) and (msg.text not in config.commands): #добавление токена
        text_msg = db_process.add_token(msg.from_user.id, msg.text, text.add_token)

    if db_process.check_status(msg.from_user.id, config.statuses[1]) and (msg.text not in config.commands): #добавление магазина
        text_msg = db_process.add_shop(msg.from_user.id, msg.text, text.change_status)

    elif db_process.check_status(msg.from_user.id, config.statuses[4]) and (msg.text not in config.commands): #добавление админа
        text_msg = text.start_text[1]
        if msg.forward_from != None:
            text_msg = db_process.add_admin(msg.from_user.id, str(msg.forward_from.id), text.admin, str(msg.forward_from.username))

    elif db_process.check_status(msg.from_user.id, config.statuses[11]) and (msg.text not in config.commands): #изменение названия магазина
        text_msg = db_process.change_name_shop(msg.from_user.id, msg.text)

    elif db_process.check_status(msg.from_user.id, config.statuses[7]) and (msg.text not in config.commands): #добавление времени запуска/остановки рекламы
        text_msg = db_process.add_time(msg.from_user.id, msg.text, text.check_time)

    if text_msg == text.check_time[1]:
        await msg.answer(text_msg)

    else:
        await msg.answer(text_msg, reply_markup=kb.menu, parse_mode="HTML")

@dp.callback_query(F.data == 'add_shop') #добавить магазин
async def request_add_shop(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[1], text.add_shop, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'list_shop') #список магазинов кнопками
async def request_add_shop(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[0], text.set_shop, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_shop_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'add_admin') #добавить админа
async def request_add_admin(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[4], text.add_admin, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'del_admin') #удалить админа
async def request_add_admin(call: CallbackQuery):
    text_msg =  text.change_status[1]
    keyb = kb.menu
    if str(kb.create_set_admin_buttons(call.message.chat.id)[1][0]) != text.check_kb:
        text_msg = db_process.change_status(call.message.chat.id, config.statuses[5], text.del_admin, 'st_b')
        keyb = kb.create_set_admin_buttons(call.message.chat.id)[0]
    await call.message.edit_text(text_msg, reply_markup=keyb)

@dp.callback_query(F.data.startswith('use_adm-')) #выбор админа
async def work_with_shop(call: CallbackQuery):
    use_adm_name = call.data.replace('use_adm-', '')
    text_msg = db_process.del_admin(call.message.chat.id, text.admin_delete, use_adm_name)
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data.startswith('dt_sh-')) #выбор магазина
async def work_with_shop(call: CallbackQuery):
    dt_sh_name = call.data.replace('dt_sh-', '')
    text_msg = db_process.change_status(call.message.chat.id, dt_sh_name, text.in_shop, 'st_sh')
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_company_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'change_name') #изменение названия магазина
async def time_add(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[11], text.change_name, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'full_time') #работа с настройками времени
async def time_add(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[00], text.full_time, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.time)

@dp.callback_query(F.data == 'time_add') #добавление времени запуска/остановки рекламы
async def time_add(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[7], text.time_add, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.menu)

@dp.callback_query(F.data == 'del_shop') #удаление магазина
async def time_add(call: CallbackQuery):
    text_msg = db_process.del_shop(call.message.chat.id, text.del_shop)
    await call.message.edit_text(text_msg, reply_markup=kb.create_set_del_shop_buttons(call.message.chat.id))

@dp.callback_query(F.data == 'main_menu') #вернуться в главное меню
async def main_menu(call: CallbackQuery):
    text_msg = db_process.change_status(call.message.chat.id, config.statuses[0], text.start_text, 'st_b')
    await call.message.edit_text(text_msg, reply_markup=kb.start)