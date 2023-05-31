import psycopg2

from create_bot import bot

DATABASE_URL = "postgres://postgres:31012002sesiD@localhost:5432/aiogram_lesson_bot"


def connect_to_db():
    global db_connection, cur
    db_connection = psycopg2.connect(DATABASE_URL, sslmode="allow")
    cur = db_connection.cursor()
    if db_connection:
        print('Подключение к базе данных произведено!')
    cur.execute("CREATE TABLE IF NOT EXISTS bot_quiz (photo TEXT, date TEXT, description TEXT, price TEXT)")
    db_connection.commit()


async def insert_data(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO bot_quiz VALUES (%s, %s, %s, %s)", tuple(data.values()))
        db_connection.commit()


async def psql_read(msg):
    cur.execute('SELECT * FROM bot_quiz')
    res = cur.fetchall()
    for ret in res:
        await bot.send_photo(msg.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')


def connect_to_db_users():
    global users_db_conn, users_cur
    users_db_conn = psycopg2.connect(DATABASE_URL, sslmode="allow")
    users_cur = users_db_conn.cursor()
    if users_db_conn:
        print('Подключение к базе данных пользователей произведено!')
    users_cur.execute("CREATE TABLE IF NOT EXISTS users1 (user_id TEXT, user_first_name TEXT, user_last_name TEXT)")
    users_db_conn.commit()


async def insert_data_users(user_id, user_first_name, user_last_name, message):
    count = 0
    users_cur.execute('SELECT * FROM users1')
    res = users_cur.fetchall()
    ap = []
    list_res = []
    for ret in res:
        count += 1
        ap.append(ret[0])
    for item in ap:
        if item not in list_res:
            list_res.append(item)
    if str(message.from_user.id) in list_res:
        users_db_conn.commit()
    else:
        users_cur.execute("INSERT INTO users1 (user_id, user_first_name, user_last_name) VALUES (%s, %s, %s)",
                          [user_id, user_first_name, user_last_name])
        users_db_conn.commit()
    if count == 0:
        users_cur.execute("INSERT INTO users1 (user_id, user_first_name, user_last_name) VALUES (%s, %s, %s)",
                          [user_id, user_first_name, user_last_name])
        users_db_conn.commit()


async def read_db_users1(msg):
    users_cur.execute('SELECT * FROM users1')
    user_fet = users_cur.fetchall()
    ap = []
    list_res = []
    for ret1 in user_fet:
        ap.append(ret1[0])
    for item in ap:
        if item not in list_res:
            list_res.append(item)
    cur.execute('SELECT * FROM bot_quiz')
    res = cur.fetchall()
    for ret in res:
        for item in list_res:
            await bot.send_photo(item, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
