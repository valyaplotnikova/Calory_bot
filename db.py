import sqlite3


connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS User(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute('DELETE FROM User')

for i in range(1, 11):
    cursor.execute('INSERT INTO User(username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', f'{i*10}', 1000)
                   )

cursor.execute('UPDATE User SET balance=500 WHERE id % 2 = 1')
cursor.execute('DELETE FROM User WHERE id % 3 = 1')

cursor.execute('SELECT username, email, age, balance FROM User WHERE age != 60')
results = cursor.fetchall()

for row in results:
    username, email, age, balance = row
    print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

# Удалите из базы данных not_telegram.db запись с id = 6.
cursor.execute('DELETE FROM User WHERE id = 6')

# Подсчитать общее количество записей.
cursor.execute('SELECT COUNT(*) FROM User')
count = cursor.fetchone()[0]

# Посчитать сумму всех балансов
cursor.execute('SELECT SUM(balance) FROM User')
sum_balance = cursor.fetchone()[0]

# Вывести в консоль средний баланс всех пользователей
cursor.execute('SELECT AVG(balance) FROM User')
avg_balance = cursor.fetchone()

print(sum_balance/count)

connection.commit()
connection.close()
