# test_product_routes.py
import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.domain.repositories import ProductRepository
from app.infrastructure.database import ProductDatabase
from app.domain.models import Product

class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.product_db = ProductDatabase()
        self.product_repo = ProductRepository(self.product_db)
        self.product_data = {'name': 'Morena', 'category': 'Coffe', 'price': 100.0}

    @patch('app.routes.product_routes.product_repo', autospec=True)
    def test_create_product(self, mock_product_repo):
        mock_product_repo.create.return_value = 1
        response = self.app.post('/products', json=self.product_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'product_id': 1})
        
    @patch('app.routes.product_routes.product_repo', autospec=True)
    def test_get_product(self, mock_product_repo):
        mock_product_repo.get.return_value = Product(1, "Morena", "Coffee", 100.0)
        
        response = self.app.get('/products/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'product_id': 1,
            'name': 'Morena',
            'category': 'Coffee',
            'price': 100.0
        })

if __name__ == '__main__':
    unittest.main()
