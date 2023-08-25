import unittest
from unittest.mock import patch
from app import app
from app.domain.repositories import ProductRepository
from app.domain.models import Product
from app.domain.models import db

class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.product_repo = ProductRepository(db)
        self.product_data = {'name': 'Morena', 'category': 'Coffe', 'price': 100.0}
        

    @patch('app.routes.product_routes.product_repo', autospec=True)
    def test_create_product(self, mock_product_repo):
        product = Product(name="Morena", category="Coffee", price=100.0)
        product.id = 11
        mock_product_repo.create.return_value = product
        response = self.app.post('/products', json=self.product_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'product_id' : 11})
        
    @patch('app.routes.product_routes.product_repo', autospec=True)
    def test_get_product(self, mock_product_repo):
        product = Product(name="Morena", category="Coffee", price=100.0)
        product.id = 11
        mock_product_repo.get.return_value = product
        
        response = self.app.get('/products/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'product_id': 11,
            'name': 'Morena',
            'category': 'Coffee',
            'price': 100.0
        })

if __name__ == '__main__':
    unittest.main()
