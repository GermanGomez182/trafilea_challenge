from app.domain.repositories import CartRepository
from flask import Blueprint, request, jsonify
from app.domain.repositories import CartRepository, ProductRepository, OrderRepository
from app.domain.services.totals_service import TotalsService
from app.domain.models import db

cart_repo = CartRepository(db)
order_repo = OrderRepository(db, cart_repo, TotalsService())
order_bp = Blueprint('order', __name__)


@order_bp.route('/carts/<int:cart_id>/orders', methods=['POST'])
def create_order_from_cart(cart_id):
    cart = cart_repo.get(cart_id)
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404
    
    order = order_repo.create(cart)
    order_totals = order.totals
    
    return jsonify({'order_totals': order_totals}), 201