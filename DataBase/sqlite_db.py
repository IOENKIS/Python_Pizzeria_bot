import sqlite3 as sq
from create_bot import bot


def sq_start():
    global base, cur
    base = sq.connect('Pizzeria.db')
    cur = base.cursor()
    if base:
        print('База данных подключенна!')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        img BLOB,
        name TEXT,
        description TEXT,
        price REAL
    )
    ''')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu (img, name, description, price) VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()

async def sql_result_state(message):
    result = cur.execute("SELECT * FROM menu ORDER BY id DESC LIMIT 1")
    for res in result:
        await bot.send_photo(message.from_user.id, res[1], f'Название: {res[2]}\nОписание: {res[3]}\nЦена: {res[-1]} грн')

async def sql_read(message):
    try:
       results = cur.execute("SELECT * FROM menu").fetchall()
       if len(results) == 0:
           await bot.send_message(message.from_user.id, 'В меню пока ничего нету')
       else:
            for ret in results:
                await bot.send_photo(message.from_user.id, ret[1], f'Название: {ret[2]}\nОписание: {ret[3]}\nЦена: {ret[-1]} грн')
    except Exception as e:
        await bot.send_message(message.from_user.id, f'Произошла ошибка {e}')

async def sql_read2():
    return cur.execute("SELECT * FROM menu").fetchall()

async def sql_delete_command(data):
    cur.execute("DELETE FROM menu WHERE name == ?", (data,))
    base.commit()

