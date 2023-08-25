from flask import Blueprint, request, jsonify
from app.domain.repositories import ProductRepository
from app.domain.models import db

product_bp = Blueprint('product', __name__)

product_repo = ProductRepository(db)

@product_bp.route('/products', methods=['POST'])
def create_product():
    product_data = request.json
    product = product_repo.create(product_data)
    return jsonify({'product_id': product.id}), 201

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = product_repo.get(product_id)
    
    if product is None:
        return jsonify({'message': 'Product not found'}), 404
    product_data = {
        'product_id': product.id,
        'name': product.name,
        'category': product.category,
        'price': product.price
    }
    
    return jsonify(product_data), 200
