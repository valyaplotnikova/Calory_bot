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
    );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        );
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


def is_included(username):
    conn = sqlite3.connect('not_telegram.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT COUNT(*) FROM Users WHERE username = ?',
        (username,)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def add_user(username, email, age):
    if not is_included(username):
        connection = sqlite3.connect('not_telegram.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
            (username, email, age, 1000)
        )
        connection.commit()
        connection.close()
