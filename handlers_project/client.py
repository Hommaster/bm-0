from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb_client
from db_bot import psql_bot

ID = 825352081


async def commands_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вас приветствует КвизБот!', reply_markup=kb_client)
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    await psql_bot.insert_data_users(user_id, user_first_name, user_last_name, message)
    await message.delete()


async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь и я отправлю тебе это в ответ!")


async def start_quiz_time(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Пятница!\n09.06.2023\n18:30')


async def registration_command_on_quiz(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Вот сслыка на форму для регистрации!')


@dp.message_handler(commands=['Меню'])
async def quiz_menu(msg: types.Message):
    await psql_bot.psql_read(msg)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(start_quiz_time, commands=['Время_начала'])
    dp.register_message_handler(registration_command_on_quiz, commands=['Регистрация'])
    dp.register_message_handler(quiz_menu, commands=['Меню'])
