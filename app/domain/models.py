class Cart:
    def __init__(self, user_id):
        self.cart_id = 0
        self.user_id = user_id
        self.products = []
        
    def add_product(self, product_id, quantity):
        self.products.append({product_id, quantity})
