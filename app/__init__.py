from flask import Flask

app = Flask(__name__)

# Blueprints
from app.routes.cart_routes import cart_bp
app.register_blueprint(cart_bp)
