import logging
from aiogram.utils import executor
from create_bot import dp
from handlers_project import client, admin, other
from db_bot import psql_bot

import os, json

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('Бот вышел в онлайн!')
    psql_bot.connect_to_db()
    psql_bot.connect_to_db_users()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

if __name__ == '__main__':
    executor.start_polling(dp)
