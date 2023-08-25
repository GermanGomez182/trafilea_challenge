class Cart:
    def __init__(self, cart_id, user_id):
        self.cart_id = cart_id
        self.user_id = user_id
        self.products = [] 
        
    def add_product(self, product_id, quantity):
        for product in self.products:
            if product['product_id'] == product_id:
                product['quantity'] += quantity
                return

        self.products.append({'product_id': product_id, 'quantity': quantity})