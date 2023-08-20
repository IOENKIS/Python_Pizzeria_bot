from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
a_b1 = KeyboardButton('Меню(Админ)')
a_b2 = KeyboardButton('Удалить(Меню)')

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(a_b1, a_b2)