from aiogram import types
from create_bot import dp

# @dp.message_handler()
async def other_words (message: types.Message):
    await message.reply(f'<b>🤷Я не знаю такой команды🤷</b>')

def register_handlers_other():
    dp.register_message_handler(other_words)