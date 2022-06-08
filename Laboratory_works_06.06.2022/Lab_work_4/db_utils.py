import sqlite3

# В этом файле описаны функции для работы приложения с базой данных

path_db = 'database.db'


def create_table():
    with sqlite3.connect(path_db) as database:
        cursor = database.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                          user_id TEXT PRIMARY KEY,
                          user TEXT)"""
                       )
        database.commit()


def insert_user(user_id, user):
    with sqlite3.connect(path_db) as database:
        cursor = database.cursor()
        cursor.execute("INSERT INTO users(user_id, user) VALUES (?, ?)", (user_id, user))
        database.commit()


def update_user(user_id, user):
    with sqlite3.connect(path_db) as database:
        cursor = database.cursor()
        cursor.execute("UPDATE users SET user = ? WHERE user_id = ?", (user, user_id))
        database.commit()


def select_id(is_id):
    with sqlite3.connect(path_db) as database:
        cursor = database.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (is_id,))
        user_id = cursor.fetchone()
        if user_id:
            return user_id[0]
        else:
            return None


def select_user(user_id):
    with sqlite3.connect(path_db) as database:
        cursor = database.cursor()
        cursor.execute("SELECT user FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return user[0]
        else:
            return None
