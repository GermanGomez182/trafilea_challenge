import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.domain.models import Cart
from app.domain.repositories import CartRepository
from app.infrastructure.database import CartDatabase

class TestCartRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.cart_repo = CartRepository(CartDatabase())
        self.cart_data = {'user_id': 'user1234'}

    @patch('app.routes.cart_routes.cart_repo', autospec=True)
    def test_create_cart(self, mock_cart_repo):
        mock_cart_repo.create.return_value = 1
        response = self.app.post('/cart', json=self.cart_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'cart_id': 1})
    
    @patch('app.routes.cart_routes.cart_repo', autospec=True)
    def test_add_product_to_cart(self, mock_cart_repo):
        cart_id = 1
        cart = Cart(user_id='user1234')
        cart.cart_id = cart_id
        mock_cart_repo.get.return_value = cart
        product_data = {'product_id': 1, 'quantity': 2}
        response = self.app.post(f'/cart/{cart_id}/add_product', json=product_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.products[0] , {product_data.get('product_id'), product_data.get('quantity')})

if __name__ == '__main__':
    unittest.main()