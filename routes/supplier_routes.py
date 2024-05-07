from flask import Blueprint, jsonify, request
from models.supplier import Supplier
from models.material import Material
from models.materials_per_supplier import MaterialsPerSupplier

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/api/suppliers')

###################################################
# Get for multiple Suppliers
###################################################
@suppliers_bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.serialize() for supplier in suppliers])

###################################################
# Get for a single Suppliers (inc. Material Data)
###################################################
@suppliers_bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.filter(Supplier.id == supplier_id).first()
    if supplier:
        materials = Material.query.join(MaterialsPerSupplier)\
                                  .join(Supplier)\
                                  .filter(MaterialsPerSupplier.supplier_id==supplier_id)\
                                  .filter(Material.id==MaterialsPerSupplier.material_id)\
                                  .add_columns(Material.id,Material.name,Material.safety_stock,Material.lot_size,Material.stock_level,MaterialsPerSupplier.min_amount,MaterialsPerSupplier.max_amount,MaterialsPerSupplier.lead_time,MaterialsPerSupplier.availability,MaterialsPerSupplier.volume_commitment)\
                                  .all()
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
                    'lead_time': material.lead_time.strftime("%H:%M:%S"),
                    'availability': material.availability,
                    'volume_commitment': material.volume_commitment,
                }
            )
        supplier_data = {
                'id': supplier.id,
                'name': supplier.name,
                'lat': supplier.lat,
                'long': supplier.long,
                'risk_index': supplier.risk_index,
                'sustainability_index':supplier.sustainability_index,
                'quality':supplier.quality,
                'reliability':supplier.reliability,
                'materials': materials_list
        }
        return jsonify(supplier_data), 200
    else:
        return jsonify({'message': f'Supplier with id {supplier_id} not found'}), 404

###################################################
# Post a single or multiple suppliers
###################################################
def create_suppliers():
    from app import db
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'error': 'JSON payload must be a list of suppliers'}), 400

    new_suppliers = []
    for supplier_data in data:
        new_supplier = Supplier(
            name=supplier_data.get('name'),
            lat=supplier_data.get('lat'),
            long=supplier_data.get('long'),
            risk_index=supplier_data.get('risk_index'),
            sustainability_index=supplier_data.get('sustainability_index'),
            quality=supplier_data.get('quality'),
            reliability=supplier_data.get('reliability')
        )
        new_suppliers.append(new_supplier)
        db.session.add(new_supplier)

    db.session.commit()

    serialized_suppliers = [supplier.serialize() for supplier in new_suppliers]
    return jsonify(serialized_suppliers), 201

###################################################
# Delete a single supplier
###################################################
@suppliers_bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    from app import db
    supplier = Supplier.query.get(supplier_id)
    if supplier:
        # Delete from the database
        MaterialsPerSupplier.query.filter_by(supplier_id=supplier_id).delete()
        
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message': 'Supplier and associated records deleted successfully'}), 200
    else:
        return jsonify({'error': 'Supplier not found'}), 404