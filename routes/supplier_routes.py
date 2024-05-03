from flask import Blueprint, jsonify, request
from models.supplier import Supplier
from models.material import Material
from models.materials_per_supplier import MaterialsPerSupplier

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/api/suppliers')

@suppliers_bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.serialize() for supplier in suppliers])

@suppliers_bp.route('/', methods=['POST'])
def create_suppliers():
    from app import db
    data = request.get_json()
    new_supplier = Supplier(name=data['name'], lat=data['lat'], long=data['long'])
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify(new_supplier.serialize()), 201


@suppliers_bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    suppliers = Supplier.query.filter(Supplier.id == supplier_id).first()
    if suppliers:
        materials = Material.query.join(MaterialsPerSupplier).join(Supplier).filter(MaterialsPerSupplier.supplier_id==supplier_id).filter(Material.id==MaterialsPerSupplier.material_id).all()
        materials_list = []
        for material in materials:
            materials_list.append(
                {
                    'id': material.id,
                    'name': material.name,
                    'safety_stock': material.safety_stock,
                    'lot_size': material.lot_size,
                    'stock_level': material.stock_level,
                    'min_amount': material.min_amount,
                    'max_amount': material.max_amount,
                    'lead_time': material.lead_time,
                    'availability': material.availability
                }
            )
        supplier_data = {
                'id': suppliers.id,
                'name': suppliers.name,
                'lat': suppliers.lat,
                'long': suppliers.long,
                'materials': materials_list
        }
        return jsonify(supplier_data), 200
    else:
        return jsonify({'message': 'Supplier not found'}), 404