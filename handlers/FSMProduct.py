from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from buttons import cancel_markup, start_markup, yes_markup
from aiogram.types import ReplyKeyboardRemove
from db import main_db

class FSMProduct(StatesGroup):
     name_product = State()
     category = State()
     size = State()
     price = State()
     product_id = State()
     photo = State()
     submit = State()


async def start_fsm_record(message: types.Message):
    await message.answer('Название продукта', reply_markup=cancel_markup)
    await FSMProduct.name_product.set()

async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text

    await FSMProduct.next()
    await message.answer('Укажите категорию: ')

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await FSMProduct.next()
    await message.answer('Укажите размер: ')

async def load_size(message: types.Message, state: FSMContext):
     async with state.proxy() as data:
         data['size'] = message.text

     await FSMProduct.next()
     await message.answer('Цена')

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await FSMProduct.next()
    await message.answer('Артикул')

async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await FSMProduct.next()
    await message.answer('Фото')

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id


    await FSMProduct.next()
    await message.answer(f'Верные ли данные?',reply_markup=yes_markup)
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название модели - {data["name_product"]}\n'
                             f'Размер - {data["size"]}\n'
                             f'Категория - {data["category"]}\n'
                             f'Стоимость - {data["price"]}\n'
                             f"Артикул - {data['product_id']}\n")


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'Да'.lower():
        async with state.proxy() as data:
            await main_db.sql_insert_product(
                name_product=data['name_product'],
                category=data['category'],
                size=data['size'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo']
            )


            await message.answer('Ваши данные в базе!')
            await state.finish()

    elif message.text.lower() == 'Нет'.lower():
        await message.answer('Хорошо, отменено!')
        await state.finish()

    else:
        await message.answer('Введите Да или Нет!')

async def cancel_fsm(message: types.Message, state: FSMContext):
    curses_state = await state.get_state()


    if curses_state is not None:
        await state.finish()
        await message.answer('Отменено!',reply_markup=start_markup)


def register_fsmproduct_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True))

    dp.register_message_handler(start_fsm_record, commands=['item_record'])
    dp.register_message_handler(load_name_product, state=FSMProduct.name_product)
    dp.register_message_handler(load_category, state=FSMProduct.category)
    dp.register_message_handler(load_size, state=FSMProduct.size)
    dp.register_message_handler(load_price, state=FSMProduct.price)
    dp.register_message_handler(load_product_id, state=FSMProduct.product_id)
    dp.register_message_handler(load_photo, state=FSMProduct.photo, content_types=['photo'])
    dp.register_message_handler(load_submit, state=FSMProduct.submit)