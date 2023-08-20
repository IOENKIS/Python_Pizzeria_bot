from aiogram import types
from keyboards import client_kb
from create_bot import dp, bot
from aiogram.dispatcher.filters import Command
from DataBase import sqlite_db


# @dp.message_handler(Command('start', ignore_caption=False))
async def start(message: types.Message):
    bot_name = await bot.get_me()
    with open('anim/pizza-welcome.tgs', 'rb') as anim:
        await message.answer_animation(anim)
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name},\nЯ <b>{bot_name.first_name}</b>, Я помогу тебе заказать пиццу',
                            reply_markup=client_kb)

# @dp.message_handler(ambda message: message.text in ('⌛Режим Роботы⌛', '📍Контакты📍', '🍕Меню🍕'))
async def buttons_client(message: types.Message):

    if message.text == '⌛Режим Роботы⌛':
       await bot.send_message(message.from_user.id, '''🍕🍕🍕🍕🍕🍕
пн  ->  11:00 - 22:00
вт  ->  11:00 - 22:00
ср  ->  11:00 - 22:00
чт  ->  11:00 - 22:00
пт  ->  11:00 - 22:00
сб  ->  11:00 - 22:00
нд  ->  11:00 - 22:00
🍕🍕🍕🍕🍕🍕''')
    elif message.text == '📍Контакты📍':
        await bot.send_message(message.from_user.id, 'Адрес: ул. Гната Юры, 6, Киев, 02000\nТелефон: 044 222 1111')
    elif message.text == '🍕Меню🍕':
        await sqlite_db.sql_read(message)


def register_handlers_client():
    dp.register_message_handler(start, Command('start'))
    dp.register_message_handler(buttons_client, lambda message: message.text in ('⌛Режим Роботы⌛', '📍Контакты📍', '🍕Меню🍕'))





