class TotalsService:
    def calculate_products_total(self, cart):
        return sum(product.product.price * product.quantity for product in cart.cart_products)
    
    def calculate_discounts_total(self, cart):
        return 0

    def calculate_shipping_total(self, cart):
        return 0

    def calculate_order_total(self, cart):
        products_total = self.calculate_products_total(cart)
        discounts_total = self.calculate_discounts_total(cart)
        shipping_total = self.calculate_shipping_total(cart)
        return products_total - discounts_total + shipping_total
