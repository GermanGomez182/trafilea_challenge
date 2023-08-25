class CartRepository:
    def __init__(self, database):
        self.database = database

    def create(self, user_id):
         return self.database.create(user_id)
    
    def get(self, cart_id):
        return self.database.find(cart_id)

    def get_by_user_id(self, user_id):
        pass
    
    def update(self, cart):
        return self.database.update(cart)
    
    def add_product(self, cart_id, product_id, quantity):
        cart = self.database.find(cart_id)
        if cart is None:
            return False

        self.database.add_product(cart_id, product_id, quantity)
        return True