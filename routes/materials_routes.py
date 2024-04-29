from flask import Blueprint, jsonify, request
from models.material import Material

material_bp = Blueprint('material', __name__, url_prefix='/api/materials')

@material_bp.route('/', methods=['GET'])
def get_materials():
    materials = Material.query.all()
    return jsonify([material.serialize() for material in materials])

@material_bp.route('/', methods=['POST'])
def create_material():
    from app import db
    data = request.get_json()
    new_material = Material(name=data['name'], main_supplier=data['main_supplier'], safety_stock=data['safety_stock'], lot_size=data['lot_size'])
    db.session.add(new_material)
    db.session.commit()
    return jsonify(new_material.serialize()), 201