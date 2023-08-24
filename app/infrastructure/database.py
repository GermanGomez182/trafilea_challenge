import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('''
    CREATE TABLE carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL
    )
''')

class CartDatabase:
    def create(self, user_id):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO carts (user_id) VALUES (?)', (user_id,))
        cart_id = cursor.lastrowid
        conn.commit()
        return cart_id