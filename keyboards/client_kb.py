from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button1 = KeyboardButton('/Время_Начала')
button2 = KeyboardButton('/Регистрация')
button3 = KeyboardButton('/Меню')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(button1).add(button2).row(button3)
