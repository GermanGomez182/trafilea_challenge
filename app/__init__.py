from flask import Flask
from app.domain.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localdb.db'

# Import the blueprints after creating the Flask app
from app.routes.cart_routes import cart_bp
from app.routes.product_routes import product_bp

app.register_blueprint(cart_bp)
app.register_blueprint(product_bp)

db.init_app(app)
with app.app_context():
    db.create_all()