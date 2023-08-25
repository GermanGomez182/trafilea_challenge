import unittest
from unittest.mock import patch
from app import app
from app.domain.models import Cart, CartProduct, Order, Product, db
from app.domain.repositories import CartRepository, OrderRepository
from app.domain.services.totals_service import TotalsService


class TestOrderRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.cart_repo = CartRepository(db)
        self.order_repo = OrderRepository(db, self.cart_repo, TotalsService())
        self.cart_data = {'user_id': 'user1234'}

    @patch('app.routes.order_routes.order_repo', autospec=True)
    @patch('app.routes.order_routes.cart_repo', autospec=True)
    def test_create_order_from_cart(self, mock_cart_repo, mock_order_repo):
        cart_id = 1
        cart = Cart(user_id=self.cart_data['user_id'])
        cart.id = cart_id
        cart.products = [
            CartProduct(product=Product(name='Product 1', price=10.0), quantity=2),
            CartProduct(product=Product(name='Product 2', price=20.0), quantity=3)
        ]
        mock_cart_repo.get.return_value = cart
        mock_order_repo.create.return_value = Order(cart_id=cart_id, totals={
            'products': 2 * 10.0 + 3 * 20.0,
            'discounts': 0,
            'shipping': 0,
            'order': 2 * 10.0 + 3 * 20.0
        })
        
        response = self.app.post(f'/carts/{cart_id}/orders')
        
        expected_order_totals = {
            'products': 2 * 10.0 + 3 * 20.0,
            'discounts': 0,
            'shipping': 0,
            'order': 2 * 10.0 + 3 * 20.0
        }
        
        mock_cart_repo.get.assert_called_once_with(cart_id)
        mock_order_repo.create.assert_called_once_with(cart)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'order_totals': expected_order_totals})

if __name__ == '__main__':
    unittest.main()