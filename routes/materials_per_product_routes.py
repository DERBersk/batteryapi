from flask import Blueprint, jsonify, request
from models.materials_per_product import MaterialsPerProduct

materials_per_product_bp = Blueprint('materials_per_product', __name__, url_prefix='/api/materials_per_product')

@materials_per_product_bp.route('/', methods=['GET'])
def get_materials_per_product():
    materials_per_product = MaterialsPerProduct.query.all()
    return jsonify([material_per_product.serialize() for material_per_product in materials_per_product])

@materials_per_product_bp.route('/', methods=['POST'])
def create_material_per_product():
    from app import db
    data = request.get_json()
    new_material_per_product = MaterialsPerProduct(material_id=data['material_id'], product_id=data['product_id'], amount=data['amount'])
    db.session.add(new_material_per_product)
    db.session.commit()
    return jsonify(new_material_per_product.serialize()), 201