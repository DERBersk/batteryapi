from flask import Blueprint, jsonify, request
from models.supplier import Supplier
from models.material import Material
from models.materials_per_supplier import MaterialsPerSupplier
from models.price import Price
from datetime import datetime

supplier_bp = Blueprint('supplier', __name__, url_prefix='/api/supplier')

###################################################
# Get for multiple Suppliers
###################################################
@supplier_bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.serialize() for supplier in suppliers])

###################################################
# Get for a single Suppliers (inc. Material Data)
###################################################
@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
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
            price = Price.query.filter(Price.supplier_id == supplier_id)\
                           .filter(Price.end_date == "")\
                           .filter(Price.material_id == material.id)\
                           .order_by(Price.cost).first()
            price_val = 0
            if price:
                price_val = price.cost
            
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
                    'price': price_val
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
                'availability':str(supplier.availability),
                'materials': materials_list
        }
        return jsonify(supplier_data), 200
    else:
        return jsonify({'message': f'Supplier with id {supplier_id} not found'}), 404

###################################################
# Post a single or multiple suppliers
###################################################
@supplier_bp.route('', methods=['POST'])
def create_or_update_suppliers():
    from app import db
    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format. Expected a list of suppliers.'}), 400

    for supplier_data in data:
        # Extract supplier data
        supplier_data = {
            'name': supplier_data.get('name'),
            'lat': supplier_data.get('lat'),
            'long': supplier_data.get('long'),
            'risk_index': supplier_data.get('risk_index'),
            'sustainability_index': supplier_data.get('sustainability_index'),
            'quality': supplier_data.get('quality'),
            'reliability': supplier_data.get('reliability'),
            'availability': (supplier_data.get('availability')=="True")|(supplier_data.get('availability') == "true")
        }

        # Create or update supplier
        if 'id' in supplier_data:
            supplier = Supplier.query.get(supplier_data['id'])
            if not supplier:
                return jsonify({'message': f'Supplier with id {supplier_data["id"]} not found'}), 404
            for key, value in supplier_data.items():
                setattr(supplier, key, value)
        else:
            supplier = Supplier(**supplier_data)

        db.session.add(supplier)

        # Extract materials data
        materials_data = supplier_data.get('materials', [])
        MaterialsPerSupplier.query.filter(MaterialsPerSupplier.supplier_id == supplier.id).delete()
        for material_data in materials_data:
            material_id = material_data.get('id')
            if material_id:
                material = Material.query.get(material_id)
                if not material:
                    return jsonify({'message': f'Material with id {material_id} not found'}), 404
            else:
                material = Material()

            material.name = material_data.get('name')
            material.safety_stock = material_data.get('safety_stock')
            material.lot_size = material_data.get('lot_size')
            material.stock_level = material_data.get('stock_level')

            # Add or update MaterialsPerSupplier
            min_amount = material_data.get('min_amount')
            max_amount = material_data.get('max_amount')
            lead_time = datetime.strptime(material_data.get('lead_time'), "%H:%M:%S").time()
            availability = material_data.get('availability')
            volume_commitment = material_data.get('volume_commitment')

            materials_per_supplier = MaterialsPerSupplier(
                supplier_id=supplier.id,
                material_id=material.id,
                min_amount=min_amount,
                max_amount=max_amount,
                lead_time=lead_time,
                availability=availability,
                volume_commitment=volume_commitment
            )
            db.session.add(material)
            db.session.add(materials_per_supplier)

    db.session.commit()

    return jsonify({'message': 'Suppliers created/updated successfully'}), 200


###################################################
# Delete a single supplier
###################################################
@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    from app import db
    supplier = Supplier.query.get(supplier_id)
    if supplier:
        # Delete from the database
        MaterialsPerSupplier.query.filter_by(MaterialsPerSupplier.supplier_id == supplier_id).delete()
        
        Price.query.filter_by(Price.supplier_id == supplier_id).delete()
        
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message': 'Supplier and associated records deleted successfully'}), 200
    else:
        return jsonify({'error': 'Supplier not found'}), 404