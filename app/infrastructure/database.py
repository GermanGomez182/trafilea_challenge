import sqlite3
from app.domain.models import Cart

class CartDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE carts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE cart_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cart_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (cart_id) REFERENCES carts (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

    def create(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO carts (user_id) VALUES (?)', (user_id,))
        cart_id = cursor.lastrowid
        self.conn.commit()
        return cart_id
    
    def find(self, cart_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM carts WHERE id = ?', (cart_id,))
        cart_data = cursor.fetchone()

        if cart_data is None:
            return None

        cart = Cart(cart_id=cart_data[0], user_id=cart_data[1])
        return cart

    def update(self, cart):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE carts SET user_id = ? WHERE id = ?', (cart.user_id, cart.cart_id))
        self.conn.commit()
        
    def add_product(self, cart_id, product_id, quantity):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO cart_products (cart_id, product_id, quantity) VALUES (?, ?, ?)',
            (cart_id, product_id, quantity)
        )
        self.conn.commit()

    def get_cart_products(self, cart_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT product_id, quantity FROM cart_products WHERE cart_id = ?', (cart_id,))
        product_data = cursor.fetchall()
        return product_data