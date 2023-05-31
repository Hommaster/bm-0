import json
import string

from aiogram import types, Dispatcher
from create_bot import bot


async def echo_message(msg: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in msg.text.split(' ')}.intersection(
            set(json.load(open('json_cenz.json')))) != set():
        await msg.reply('Не используйте мат!')
        await msg.delete()
    else:
        await bot.send_message(msg.from_user.id, msg.text)


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_message)
