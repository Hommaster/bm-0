from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db_bot import psql_bot

from create_bot import dp
from keyboards import admin_kb, kb_client

ID = 387111575


class FSMAdmin(StatesGroup):
    photo = State()
    date = State()
    description = State()
    price = State()


async def ready_upload_to_bot_new_quiz(msg: types.Message):
    if msg.from_user.id == ID:
        await FSMAdmin.photo.set()
        await msg.reply('Жду фотографию!')
    else:
        await msg.reply('Вы не администратор!')


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def upload_photo(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = msg.photo[0].file_id
        await FSMAdmin.next()
        await msg.reply('Отправте дату игры!')
    else:
        await msg.reply('Вы не администратор!')


async def upload_date(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ID:
        async with state.proxy() as data:
            data['date'] = msg.text
        await FSMAdmin.next()
        await msg.reply('Где будет проходить игра?')
    else:
        await msg.reply('Вы не администратор!')


async def upload_price(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = msg.text
        await FSMAdmin.next()
        await msg.reply('Мне необходима стоимость игры!')
    else:
        await msg.reply('Вы не администратор!')


async def upload_description(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(msg.text)
        await psql_bot.insert_data(state)
        await state.finish()
    else:
        await msg.reply('Вы не администратор!')


async def cancel_handler(msg: types.Message, state=FSMContext):
    if msg.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await msg.reply('Откат произведен')
    else:
        await msg.reply('Вы не администратор!')


async def send_anons(msg: types.Message):
    if msg.from_user.id == ID:
        await psql_bot.read_db_users1(msg)


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(ready_upload_to_bot_new_quiz, commands=['Загрузить'], state=None)
    dp.register_message_handler(upload_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(upload_date, state=FSMAdmin.date)
    dp.register_message_handler(upload_price, state=FSMAdmin.description)
    dp.register_message_handler(upload_description, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(cancel_handler, state="*", commands='Отмена')
    dp.register_message_handler(send_anons, commands=['Рассылка'])