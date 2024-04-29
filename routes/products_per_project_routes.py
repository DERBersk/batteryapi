from flask import Blueprint, jsonify, request
from models.products_per_project import ProductsPerProject

products_per_project_bp = Blueprint('products_per_project', __name__, url_prefix='/api/products_per_project')

@products_per_project_bp.route('/', methods=['GET'])
def get_products_per_project():
    products_per_project = ProductsPerProject.query.all()
    return jsonify([product_per_project.serialize() for product_per_project in products_per_project])

@products_per_project_bp.route('/', methods=['POST'])
def create_product_per_project():
    from app import db
    data = request.get_json()
    new_product_per_project = ProductsPerProject(product_id=data['product_id'], project_id=data['project_id'], start=data['start'], end=data['end'], amount=data['amount'], strategy=data['strategy'])
    db.session.add(new_product_per_project)
    db.session.commit()
    return jsonify(new_product_per_project.serialize()), 201