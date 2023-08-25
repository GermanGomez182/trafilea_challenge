class TotalsService:
    def calculate_products_total(self, cart):
        return sum(cart_product.product.price * cart_product.quantity for cart_product in cart.cart_products)
    
    def calculate_discounts_total(self, cart):
        free_coffee_rule_discount = self.calculate_free_coffee_discount(cart)
        accessories_discount = self.calculate_accessories_discount(cart)
        return free_coffee_rule_discount + accessories_discount
    
    def calculate_shipping_total(self, cart):
        #standard shipping = $20
        if self.is_equipment_shipping_discount(cart):
            return 0
        else:
            return 20.0
    
    def calculate_order_total(self, cart):
        products_total = self.calculate_products_total(cart)
        discounts_total = self.calculate_discounts_total(cart)
        shipping_total = self.calculate_shipping_total(cart)
        return products_total - discounts_total + shipping_total
    
    def calculate_free_coffee_discount(self, cart):
        # Calculate the discount for the "Buy 2 or more Coffee, get one free" rule
        coffee_products = [cart_product for cart_product in cart.cart_products if cart_product.product.category == 'Coffee']
        num_coffee_products = sum(cart_product.quantity for cart_product in coffee_products)
        
        coffee_discount = 0.0
        while num_coffee_products >= 2:
            num_coffee_products -= 2
            coffee_discount += min(cart_product.product.price for cart_product in coffee_products)
        
        return coffee_discount
        
    def is_equipment_shipping_discount(self, cart):
        # "Buy more than 3 Equipment, get free shipping" rule
        equipment_products = [cart_product for cart_product in cart.cart_products if cart_product.product.category == 'Equipment']
        num_equipment_products = sum(cart_product.quantity for cart_product in equipment_products)
        
        return num_equipment_products > 3

    
    def calculate_accessories_discount(self, cart):
        # "Spend more than 70 dollars on Accessories, get 10% discount" rule
        accessories_products = [cart_product for cart_product in cart.cart_products if cart_product.product.category == 'Accessories']
        total_accessories_spent = sum(cart_product.product.price * cart_product.quantity for cart_product in accessories_products)
        
        if total_accessories_spent > 70:
            return 0.10 * total_accessories_spent
        return 0.0