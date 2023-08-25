from flask import Blueprint, request, jsonify
from app.domain.repositories import CartRepository
from app.infrastructure.database import CartDatabase
from app.domain.models import Cart
import json

cart_bp = Blueprint('cart', __name__)

cart_repo = CartRepository(CartDatabase())

@cart_bp.route('/carts', methods=['POST'])
def create_cart():
    user_id = request.json.get('user_id')
    cart_id = cart_repo.create(user_id)
    return jsonify({'cart_id': cart_id}), 201

@cart_bp.route('/carts/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    cart = cart_repo.get(cart_id)
    if cart is None:
        return jsonify({'message': 'Cart not found'}), 404

    cart_data = {
        'cart_id': cart.cart_id,
        'user_id': cart.user_id,
        'products': cart.products
    }
    return jsonify(cart_data), 200

@cart_bp.route('/carts/<int:cart_id>/add_product', methods=['POST'])
def add_product_to_cart(cart_id):
    product_data = request.json
    cart = cart_repo.get(cart_id)
    if cart is None:
        return jsonify({'message': 'Cart not found'}), 404

    success = cart_repo.add_product(cart_id, product_data['product_id'], product_data['quantity'])
    if not success:
        return jsonify({'message': 'Failed to add product to cart'}), 500

    return jsonify({'message': 'Product added to cart'}), 200



