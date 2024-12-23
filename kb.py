from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, WebAppInfo

import config
import db

db_process = db.options_db()

def create_set_shop_buttons(id_user):
    start_button = []

    tuple_name_shop = db_process.create_tuple_db_posizione(id_user, config.name_posizione[5])

    if tuple_name_shop[0] != None and len(tuple_name_shop) > 0:
        for i in tuple_name_shop[0].split('/')[:-1]:
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dt_sh-{i}')])

    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_set_company_buttons(id_user):
    start_button = []

    chek_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split('/')[:-1]
    use_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

    id_use_shop = chek_shop.index(use_shop)

    tuple_name_company = db_process.create_tuple_db_posizione(id_user, config.name_posizione[12])

    if tuple_name_company[0] != None and len(tuple_name_company) > 0:
        for i in tuple_name_company[0].split('/')[:-1][id_use_shop].split(';'):
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'dt_cp-{i}')])

    start_button.append([InlineKeyboardButton(text='Изменить название', callback_data='change_name')])
    start_button.append([InlineKeyboardButton(text='Удалить магазин', callback_data='del_shop')])
    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_set_del_shop_buttons(id_user):
    start_button = []

    tuple_name_shop = db_process.create_tuple_db_posizione(id_user, config.name_posizione[5])

    if tuple_name_shop[0] != None and len(tuple_name_shop) > 0:
        for i in tuple_name_shop[0].split(';'):
            start_button.append([InlineKeyboardButton(text=i, callback_data=f'del_sh-{i}')])

    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb

def create_set_admin_buttons(id_user):
    start_button = []

    tuple_admin = db_process.create_tuple_db_posizione(id_user, config.name_posizione[1])

    chek_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[5]))[0].split(';')
    use_shop = list(db_process.create_tuple_db_posizione(id_user, config.name_posizione[9]))[0]

    id_use_shop = chek_shop.index(use_shop)

    if tuple_admin[0] != None and len(tuple_admin) > 0:
        admin = tuple_admin[0].split('/')[id_use_shop].split(';')
        for i in range(len(admin)):
            if admin[i] != '':
                start_button.append([InlineKeyboardButton(text=admin[i], callback_data=f'use_adm-{admin[i]}')])
            else:
                pass

    start_button.append([InlineKeyboardButton(text='Главное меню', callback_data='main_menu')])
    start_kb = InlineKeyboardMarkup(inline_keyboard=start_button)
    return start_kb, start_button


main_menu = [
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu'),
     ],
]

in_shop = [
    [InlineKeyboardButton(text='Отложенный запуск рекламы', callback_data='full_time')
     ],
    [InlineKeyboardButton(text='Зафиксировать ключевые запросы', callback_data='key_query')
     ],
    [InlineKeyboardButton(text='Добавить админа', callback_data='add_admin')
     ],
    [InlineKeyboardButton(text='Удалить админа', callback_data='del_admin')
     ],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
     ],
]

time_button = [
    [InlineKeyboardButton(text='Запуск по времени', callback_data='add_shop')
     ],
    [InlineKeyboardButton(text='Старт рекламы', callback_data='list_shop')
     ],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
     ],
]

start_button = [
    [InlineKeyboardButton(text='Добавить магазин', callback_data='add_shop')
     ],
    [InlineKeyboardButton(text='Список магазинов', callback_data='list_shop')
     ],
    [InlineKeyboardButton(text='Тарифы', callback_data='tariffs')
     ],
]

in_shop_kb = InlineKeyboardMarkup(inline_keyboard=in_shop)
menu = InlineKeyboardMarkup(inline_keyboard=main_menu)
start = InlineKeyboardMarkup(inline_keyboard=start_button)
time = InlineKeyboardMarkup(inline_keyboard=time_button)

# start_button.append([InlineKeyboardButton(text='Добавить магазин', callback_data='add_shop')])
# start_button.append([InlineKeyboardButton(text='Удалить магазин', callback_data='del_shop')])