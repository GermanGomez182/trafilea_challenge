import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.domain.models import Cart, Product, Order
from app.domain.repositories import CartRepository, ProductRepository, OrderRepository
from app.domain.services.totals_service import TotalsService
from app.domain.models import db

class TestOrderRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)
        self.order_repo = OrderRepository(db, self.cart_repo, TotalsService(), self.product_repo)
        self.cart_data = {'user_id': 'user1234'}
        
        self.product = Product(name="Coffee", category="Coffee", price=10.0)
        self.product.id = 1
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    @patch('app.routes.order_routes.cart_repo', autospec=True)
    @patch('app.routes.order_routes.order_repo', autospec=True)
    def test_create_order_from_cart(self, mock_order_repo, mock_cart_repo):        
        cart_id = 33
        cart = Cart(user_id=self.cart_data['user_id'])
        cart.id = cart_id
        mock_cart_repo.get.return_value = cart
        
        order_id = 1
        order = Order(cart.id, totals={'products': 100.0, 'discounts': 10.0, 'shipping': 0.0, 'order': 90.0})
        order.id = order_id
        mock_order_repo.create.return_value = order
        
        response = self.app.post('/carts/1/orders')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'order_totals': {'products': 100.0, 'discounts': 10.0, 'shipping': 0.0, 'order': 90.0}})

if __name__ == '__main__':
    unittest.main()
