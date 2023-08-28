from app.domain.models import Cart, Product, CartProduct, Order
from app.domain.models import Order
from app.exceptions import OrderCreationError



class CartRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user_id):
        cart = Cart(user_id=user_id)
        self.db.session.add(cart)
        self.db.session.commit()
        return cart

    def get(self, cart_id):
        return Cart.query.get(cart_id)

    def add_product(self, cart, product, quantity):
        try:
            cart_product = CartProduct(cart=cart, product=product, quantity=quantity)
            self.db.session.add(cart_product)
            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            return False

    def modify_product_quantity(self, cart, product_id, new_quantity):
            cart_product = self.db.session.query(CartProduct).filter_by(cart=cart, product_id=product_id).first()
            if cart_product:
                cart_product.quantity = new_quantity
                self.db.session.commit()
                return True
            return False


class ProductRepository:
    def __init__(self, db):
        self.db = db

    def create(self, product_data):
        product = Product(
                name=product_data['name'],
                category=product_data['category'],
                price=product_data['price']
                )
        self.db.session.add(product)
        self.db.session.commit()
        return product

    def get(self, product_id):
        return Product.query.get(product_id)
    

class OrderRepository:
    def __init__(self, db, cart_repo, totals_service, product_repo):
        self.db = db
        self.cart_repo = cart_repo
        self.totals_service = totals_service
        self.product_repo = product_repo
    
    def create(self, cart):
        existing_order = self.get_order_by_cart(cart.id)
        if existing_order:
            
            raise OrderCreationError("An order already exists for this cart.")
        coffee_discount = self.totals_service.calculate_free_coffee_discount(cart)
        
        if coffee_discount > 0:
            # Find the first coffee product in the cart and increment its quantity
            coffee_product = next((cp for cp in cart.cart_products if cp.product.category == 'Coffee'), None)
            if coffee_product:
                coffee_product.quantity += 1
             
        products_total = self.totals_service.calculate_products_total(cart)
        discounts_total = self.totals_service.calculate_discounts_total(cart)
        shipping_total = self.totals_service.calculate_shipping_total(cart)
        order_total = self.totals_service.calculate_order_total(cart)
   
        totals = {
            'products': products_total,
            'discounts': discounts_total,
            'shipping': shipping_total,
            'order': order_total
        }
        
        order = Order(cart_id=cart.id, totals=totals)
        self.db.session.add(order)
        self.db.session.commit()
        return order
    
    def get_order_by_cart(self, cart_id):
        return self.db.session.query(Order).filter_by(cart_id=cart_id).first()
