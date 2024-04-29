from flask import Blueprint, jsonify, request
from models.supplier import Supplier

supplier_bp = Blueprint('supplier', __name__, url_prefix='/api/suppliers')

@supplier_bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.serialize() for supplier in suppliers])

@supplier_bp.route('/', methods=['POST'])
def create_supplier():
    from app import db
    data = request.get_json()
    new_supplier = Supplier(name=data['name'], lat=data['lat'], long=data['long'])
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify(new_supplier.serialize()), 201