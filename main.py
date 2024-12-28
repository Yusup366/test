from aiogram import  executor
from config import bot, dp, Admins
import logging
from handlers import command,FSMProduct,send_products
import buttons
from db import main_db

async def on_startup(_):
    for admin in Admins:
        await  bot.send_message(chat_id=admin, text='Бот включен',
                                reply_markup=buttons.start_markup)
    await main_db.DataBase_creatr()


async def on_shutdown(_):
    for admin in Admins:
        await  bot.send_message(chat_id=admin, text='Бот выключен')

command.register_commands_handlers(dp)
FSMProduct.register_fsmproduct_handlers(dp)
send_products.register_handlers(dp)





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup,
                           on_shutdown=on_shutdown)




