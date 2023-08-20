from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('🍕Меню🍕')
b2 = KeyboardButton('⌛Режим Роботы⌛')
b3 = KeyboardButton('📍Контакты📍')

client_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(b1, b2, b3)

