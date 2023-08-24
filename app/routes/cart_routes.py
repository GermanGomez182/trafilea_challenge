from flask import Blueprint, request, jsonify
from app.domain.repositories import CartRepository
from app.infrastructure.database import CartDatabase
from app.domain.models import Cart
import json

cart_bp = Blueprint('cart', __name__)

cart_repo = CartRepository(CartDatabase())

@cart_bp.route('/cart', methods=['POST'])
def create_cart():
    user_id = request.json.get('user_id')
    cart_id = cart_repo.create(user_id)
    return jsonify({'cart_id': cart_id}), 201
