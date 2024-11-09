
import sqlite3
connection = sqlite3.connect('database_14_5.db')
cursor = connection.cursor()



# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:

# initiate_db дополните созданием # таблицы Users, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
# id - # целое число, первичный ключ
# username - текст (не пустой)
# email - текст (не пустой)
# age - целое число (не пустой)
# balance - целое число (не пустой)

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL)  
         ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS  Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)    
    ''')

# add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
# Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
# Баланс у новых пользователей всегда равен 1000. Для добавления pаписей в таблице используйте SQL запрос.
def add_users(username,email,age,balance=1000):
    cursor.execute('INSERT INTO Users  (username,email,age,balance) VALUES(?,?,?,?)', (username,email,age,balance))
    connection.commit()



# is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users,
# в противном случае False. Для получения записей используйте SQL запрос.

def is_include(username):
    is_incl = bool(cursor.execute(f'SELECT username FROM Users WHERE username=?',(username,)).fetchone())
    connection.commit()
    return is_incl


# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.
def get_all_products():
    cursor.execute('SELECT  title, description, price FROM Products')
    products = cursor.fetchall()
    connection.commit()
    return products

initiate_db()

# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
if __name__=='__main__':
    for i in range(1, 5):
        cursor.execute("INSERT INTO Products(title, description, price) VALUES(?,?,?)",
                   (f'Продукт{i}', f'Описание{i}', f'{i*100}'))

# Перед запуском бота пополните вашу таблицу Users 4 или более записями для последующего вывода в чате Telegram-бота.

    add_users('Dmitri','dima@yandex.ru',23)
    add_users('Anya','anya@yandex.ru', 16)
    add_users('Lilya','lilya@yandex.ru',22)
    add_users('Kolya','kolya@yandex.ru',14)

    connection.commit()






