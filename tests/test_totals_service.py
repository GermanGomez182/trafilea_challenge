import unittest
from unittest.mock import Mock
from app.domain.services.totals_service import TotalsService
from app.domain.models import Cart, CartProduct, Product

class TestTotalsService(unittest.TestCase):
    def setUp(self):
        self.service = TotalsService()
        
        # Create sample products for testing
        self.product_coffee = Product(id=1, name="Coffee", category="Coffee", price=10.0)
        self.product_equipment = Product(id=2, name="Equipment", category="Equipment", price=50.0)
        self.product_accessories = Product(id=3, name="Accessories", category="Accessories", price=30.0)
    
    def test_calculate_products_total(self):
        cart = Cart()
        cart.cart_products = [
            CartProduct(product=self.product_coffee, quantity=2),
            CartProduct(product=self.product_equipment, quantity=1),
            CartProduct(product=self.product_accessories, quantity=3)
        ]
        
        total = self.service.calculate_products_total(cart)
        expected_total = 2 * 10.0 + 1 * 50.0 + 3 * 30.0
        self.assertEqual(total, expected_total)
        
    def test_calculate_free_coffee_discount(self):
        cart = Cart()
        cart.cart_products = [
            CartProduct(product=self.product_coffee, quantity=3)
        ]
        
        discount = self.service.calculate_free_coffee_discount(cart)
        expected_discount = 10 
        self.assertEqual(discount, expected_discount)
        
    def test_is_equipment_shipping_discount(self):
        cart = Cart()
        cart.cart_products = [
            CartProduct(product=self.product_equipment, quantity=4)
        ]
        
        is_discount = self.service.is_equipment_shipping_discount(cart)
        self.assertTrue(is_discount)
        
    def test_calculate_accessories_discount(self):
        cart = Cart()
        cart.cart_products = [
            CartProduct(product=self.product_accessories, quantity=3)
        ]
        
        discount = self.service.calculate_accessories_discount(cart)
        expected_discount = 0.10 * (3 * 30.0)
        self.assertEqual(discount, expected_discount)

if __name__ == '__main__':
    unittest.main()
