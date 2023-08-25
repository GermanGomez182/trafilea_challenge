import unittest
from unittest.mock import patch
from app import app
from app.domain.models import Cart, Product
from app.domain.repositories import CartRepository, ProductRepository
from app.domain.models import db

class TestCartRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)
        self.cart_data = {'user_id': 'user1234'}

    @patch('app.routes.cart_routes.cart_repo', autospec=True)
    def test_create_cart(self, mock_cart_repo):
        cart_id = 33
        cart = Cart(user_id=self.cart_data['user_id'])
        cart.id = cart_id
        mock_cart_repo.create.return_value = cart
        response = self.app.post('/carts', json=self.cart_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'cart_id': 33})
    
    
    @patch('app.routes.cart_routes.product_repo', autospec=True)
    @patch('app.routes.cart_routes.cart_repo', autospec=True)
    def test_add_product_to_cart(self, mock_cart_repo, mock_product_repo):
        cart_id = 1
        cart = Cart(user_id=self.cart_data['user_id'])
        cart.id = cart_id
        mock_cart_repo.get.return_value = cart
        mock_cart_repo.create.return_value = cart
        mock_cart_repo.add_product.return_value = True
        product_data = {'product_id': 1, 'quantity': 3}
        product = Product(name="Sugar", category="Coffee", price=11.0)
        mock_product_repo.get.return_value = product
        
        response = self.app.post(f'/carts/{cart_id}/add_product', json=product_data)
  
        mock_product_repo.get.assert_called_once_with(product_data['product_id'])
        mock_cart_repo.get.assert_called_once_with(cart_id)
        mock_cart_repo.add_product.assert_called_once_with(cart, product, product_data['quantity'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Product added to cart'})


    @patch('app.routes.cart_routes.cart_repo', autospec=True)
    def test_get_cart(self, mock_cart_repo):
        cart_id = 1
        cart = Cart(user_id='user1234')
        cart.id = cart_id
        cart.products = []
        mock_cart_repo.get.return_value = cart

        response = self.app.get('/carts/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'cart_id': 1,
            'user_id': 'user1234',
            'products': []
        })
        
    
    @patch('app.routes.cart_routes.cart_repo', autospec=True)
    def test_modify_product_quantity(self, mock_cart_repo):
        cart_id = 1
        cart = Cart(user_id=self.cart_data['user_id'])
        cart.id = cart_id
        mock_cart_repo.get.return_value = cart
        
        product_id = 1
        new_quantity = 5
        
        response = self.app.put(f'/carts/{cart_id}/modify_product_quantity/{product_id}', json={'quantity': new_quantity})
        
        mock_cart_repo.get.assert_called_once_with(cart_id)
        mock_cart_repo.modify_product_quantity.assert_called_once_with(cart, product_id, new_quantity)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Product quantity modified'})


if __name__ == '__main__':
    unittest.main()
