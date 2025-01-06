import sqlite3


def initiate_db():
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Product')
    results = cursor.fetchall()
    connection.commit()
    connection.close()
    return results


def complete_db():
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    for i in range(1, 5):
        cursor.execute('INSERT INTO Product(title, description, price) VALUES(?, ?, ?)',
                   (f'Ежедневник{i}', f'описание {i}', f'{i*100}'))
    connection.commit()
    connection.close()


def drop_db():
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Product')
    connection.commit()
    connection.close()
