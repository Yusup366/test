from aiogram import types, Dispatcher
import os
from config import bot





async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет! Я бот для управления заказами .'
                                )

async def info_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Этот бот помогает управлят товарами и оформлять заказы.')




def register_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_handler, commands=['info'])