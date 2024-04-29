from flask import Blueprint, jsonify, request
from models.materials_per_supplier import MaterialsPerSupplier

materials_per_supplier_bp = Blueprint('materials_per_supplier', __name__, url_prefix='/api/materials_per_supplier')

@materials_per_supplier_bp.route('/', methods=['GET'])
def get_materials_per_supplier():
    materials_per_supplier = MaterialsPerSupplier.query.all()
    return jsonify([material_per_supplier.serialize() for material_per_supplier in materials_per_supplier])

@materials_per_supplier_bp.route('/', methods=['POST'])
def create_material_per_supplier():
    from app import db
    data = request.get_json()
    new_material_per_supplier = MaterialsPerSupplier(material_id=data['material_id'], supplier_id=data['supplier_id'], cost=data['cost'], unit=data['unit'], transportation_cost=data['transportation_cost'], delivery_time=data['delivery_time'], min_amount=data['min_amount'])
    db.session.add(new_material_per_supplier)
    db.session.commit()
    return jsonify(new_material_per_supplier.serialize()), 201