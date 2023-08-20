from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keyboards import admin_kb
from DataBase import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None

# Прописываем состояния
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    prise = State()
    schedule = State()


# Проверка на админа
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command (message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEHd0lj05BQjxtuwcbDo8HQ5HANryykEAACfQAD98zUGG_VX5-JRgiWLQQ')
    await bot.send_message(message.from_user.id, 'Приветствую, Админ!', reply_markup=admin_kb)
    await message.delete()

# Диалог для админа(Меню) + кнопки
# @dp.message_handler(commands='Меню(Админ)', state=None)
async def admin_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply(f'<b>Загрузи фото</b>')

# Ловим первое сообщение(Меню) + массив(словарь)
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            await FSMAdmin.next()
            await message.reply('<b>Введи название пицци</b>')

# Ловим второе сообщение(Меню) + словарь
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
            await FSMAdmin.next()
            await message.reply('<b>Введи описание пицци</b>')

# Ловим третье сообщение(Меню) + словарь
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
            await FSMAdmin.next()
            await message.reply('<b>Напоследок, введи цену</b>')

# Ловим последнее, четвертое сообщение(Меню) + словарь
# @dp.message_handler(state=FSMAdmin.prise)
async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
            
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await bot.send_message(message.from_user.id, '<b>Готово!</b>, Вот результат:')
        await sqlite_db.sql_result_state(message)


# Выход с состояния
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals = 'отмена', ignore_case = True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОТМЭНА')

# @dp.callback_query_handler(Text(x.data and x.data.startswith('del ')))
async def delete_callback_db(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


# @dp.message_handler(commands = 'Удалить(Меню)')
async def delete_butt(message: types.Message):
    if message.from_user.id == ID:
        try:
            read = await sqlite_db.sql_read2()
            if read:
                for ret in read:
                    await bot.send_photo(message.from_user.id, ret[1], f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[-1]} грн',
                                         reply_markup=InlineKeyboardMarkup(). \
                                         add(InlineKeyboardButton(f'Удалить {ret[2]}', callback_data=(f'del {ret[2]}'))))
            else:
                await bot.send_message(message.from_user.id, 'Нечего удалять🤷')
        except Exception as e:
            await bot.send_message(message.from_user.id, f'Произошла ошибка: {e}')




# Регистрируем хендлеры
def register_handlers_admin ():
    dp.register_message_handler(admin_start, lambda message: message.text in 'Меню(Админ)', state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.prise)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals = 'отмена', ignore_case = True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(delete_callback_db,lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_butt, lambda message: message.text in 'Удалить(Меню)')

