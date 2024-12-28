import sqlite3
from db import queries


db = sqlite3.connect('db/product.sqlite3')
cursor = db.cursor()

async def DataBase_creatr():
    if db:
        print('База данных подключена!')
    cursor.execute(queries.CREATE_TABLE_product)

async def sql_insert_product(name_product, category, size, price, product_id, photo):
    cursor.execute(queries.INSERT_product_QUERY,(
        name_product, category, size, price, product_id, photo
    ))
    db.commit()

