from app.domain.models import Cart, Product, CartProduct

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