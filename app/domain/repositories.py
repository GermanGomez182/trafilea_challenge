from app.domain.models import Cart, Product
from app.infrastructure.database import ProductDatabase
class CartRepository:
    def __init__(self, database):
        self.database = database
        self.product_repo = ProductRepository(ProductDatabase())

    def create(self, user_id):
         return self.database.create(user_id)
    
    def get(self, cart_id):
        cart_data = self.database.find(cart_id)
        if cart_data is None:
            return None

        cart_products_data = self.database.get_cart_products(cart_id)
        cart = Cart(
            cart_id=cart_data['cart_id'],
            user_id=cart_data['user_id']
        )
        
        for product_data in cart_products_data:
            print(product_data)
            product_id = product_data[0]
            quantity = product_data[1]
            product = self.product_repo.get(product_id)
            if product is not None:
                cart.add_product(product, quantity)
        return cart

    def get_by_user_id(self, user_id):
        pass
    
    def update(self, cart):
        return self.database.update(cart)
    
    def add_product(self, cart_id, product_id, quantity):
        cart = self.database.find(cart_id)
        product = self.product_repo.get(product_id)
        if cart is None or product is None:
            return False

        self.database.add_product(cart_id, product_id, quantity)
        return True
    
    
class ProductRepository:
    def __init__(self, database):
        self.database = database

    def create(self, product_data):
        return self.database.create(product_data)
    
    def get(self, product_id):
        product_data = self.database.find(product_id)
        if product_data is None:
            return None

        product = Product(
            product_id=product_data['product_id'],
            name=product_data['name'],
            category=product_data['category'],
            price=product_data['price']
        )
        return product