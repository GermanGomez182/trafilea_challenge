from flask import Flask

app = Flask(__name__)

# Blueprints
from app.routes.cart_routes import cart_bp
from app.routes.product_routes import product_bp

app.register_blueprint(cart_bp)
app.register_blueprint(product_bp)
