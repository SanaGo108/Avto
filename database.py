import sqlite3


def create_db():
    """Создает базу данных и таблицы"""
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS car_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT,
        model TEXT,
        price INTEGER,
        collateral_value INTEGER
    )''')

    conn.commit()
    conn.close()


def insert_car_price(make, model, price, collateral_value):
    """Вставляет данные в таблицу"""
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()

    c.execute('''INSERT INTO car_prices (make, model, price, collateral_value)
                 VALUES (?, ?, ?, ?)''', (make, model, price, collateral_value))

    conn.commit()
    conn.close()


def fetch_car_prices():
    """Получает все данные из таблицы"""
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()

    c.execute('SELECT * FROM car_prices')
    data = c.fetchall()

    conn.close()

    return data
