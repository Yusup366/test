CREATE_TABLE_product = """
    CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    category TEXT,
    size TEXT,
    price TEXT,
    product_id TEXT,
    photo TEXT,
    submit TEXT
    )
"""



INSERT_product_QUERY = """
    INSERT INTO store (name_product, category, size, price, product_id, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""