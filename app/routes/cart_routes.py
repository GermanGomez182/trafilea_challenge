from flask import Blueprint, request, jsonify
from app.domain.repositories import CartRepository, ProductRepository
from app.domain.models import db

cart_bp = Blueprint('cart', __name__)

product_repo = ProductRepository(db)
cart_repo = CartRepository(db)

@cart_bp.route('/carts', methods=['POST'])
def create_cart():
    user_id = request.json.get('user_id')
    cart = cart_repo.create(user_id)
    return jsonify({'cart_id': cart.id}), 201


@cart_bp.route('/carts/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    cart = cart_repo.get(cart_id)
    if cart is None:
        return jsonify({'message': 'Cart not found'}), 404

    cart_data = {
        'cart_id': cart.id,
        'user_id': cart.user_id,
        'products': [{'product_id': product_cart.product.id,
                      'product': product_cart.product.name,
                      'category': product_cart.product.category,
                      'quantity': product_cart.quantity} for product_cart in cart.cart_products]
    }
    return jsonify(cart_data), 200


@cart_bp.route('/carts/<int:cart_id>/add_product', methods=['POST'])
def add_product_to_cart(cart_id):
    product_data = request.json
    cart = cart_repo.get(cart_id)
    if cart is None:
        return jsonify({'message': 'Cart not found'}), 404
    product = product_repo.get(product_data['product_id'])
    if product is None:
        return jsonify({'message': 'Product not found'}), 404
    
    success = cart_repo.add_product(cart, product, product_data['quantity'])
    if not success:
        return jsonify({'message': 'Failed to add product to cart'}), 500

    return jsonify({'message': 'Product added to cart'}), 200

@cart_bp.route('/carts/<int:cart_id>/modify_product_quantity/<int:product_id>', methods=['PUT'])
def modify_product_quantity(cart_id, product_id):
    new_quantity = request.json.get('quantity')

    cart = cart_repo.get(cart_id)
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404

    success = cart_repo.modify_product_quantity(cart, product_id, new_quantity)
    if success:
        return jsonify({'message': 'Product quantity modified'}), 200
    else:
        return jsonify({'message': 'Product not found in cart'}), 404
