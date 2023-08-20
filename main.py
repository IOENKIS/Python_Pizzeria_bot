from aiogram import executor
from create_bot import dp
from DataBase import sqlite_db

# Стартовое сообщение
async def on_startup(_):
    print('Бот в онлайне!')
    sqlite_db.sq_start()

# Регистрация хендлеров
from handlers import admin, client, other
client.register_handlers_client()
admin.register_handlers_admin()
other.register_handlers_other()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

