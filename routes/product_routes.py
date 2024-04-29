from flask import Blueprint, jsonify, request
from models.product import Product

product_bp = Blueprint('product', __name__, url_prefix='/api/products')

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@product_bp.route('/', methods=['POST'])
def create_product():
    from app import db
    data = request.get_json()
    new_product = Product(name=data['name'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.serialize()), 201