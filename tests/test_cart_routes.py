import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.domain.models import Cart
from app.domain.repositories import CartRepository
from app.infrastructure.database import CartDatabase

class TestCartRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.cart_db = CartDatabase()
        self.cart_repo = CartRepository(self.cart_db)
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
        cart = Cart(cart_id, user_id='user1234')
        mock_cart_repo.get.return_value = cart

        product_data = {'product_id': 1, 'quantity': 3}

        with patch.object(mock_cart_repo, 'add_product') as mock_add_product:
            response = self.app.post(f'/cart/{cart_id}/add_product', json=product_data)

            mock_add_product.assert_called_once_with(cart_id, product_data['product_id'], product_data['quantity'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'message': 'Product added to cart'})
    
        
    @patch('app.routes.cart_routes.cart_repo', autospec=True)
    def test_get_cart(self, mock_cart_repo):
        cart_id = 1
        cart = Cart(cart_id, user_id='user1234')
        cart.cart_id = 1
        cart.products = []
        mock_cart_repo.get.return_value = cart

        response = self.app.get('/cart/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'cart_id': 1,
            'user_id': 'user1234',
            'products': []
        })

if __name__ == '__main__':
    unittest.main()
