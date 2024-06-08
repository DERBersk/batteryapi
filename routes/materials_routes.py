# import external packages
from flask import Blueprint, jsonify, request
# import models
from models.material import Material
from models.materials_per_supplier import MaterialsPerSupplier
from models.materials_per_product import MaterialsPerProduct
from models.price import Price

material_bp = Blueprint('material', __name__, url_prefix='/api/materials')

###################################################
# Get for multiple Materials
###################################################
@material_bp.route('/', methods=['GET'])
def get_materials():
    materials = Material.query.filter()
    return jsonify([material.serialize() for material in materials])

###################################################
# Get for a single Material
###################################################
@material_bp.route('/<int:material_id>', methods=['GET'])
def get_material(material_id):
    material = Material.query.filter(Material.id == material_id).first()
    if material:
        return jsonify(material.serialize())
    else:
        return jsonify({'message': f'Material with id {material_id} not found'}), 404

###################################################
# Post a single or multiple materials
###################################################
def create_or_update_materials():
    from app import db
    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format. Expected a list of materials.'}), 400

    for material_data in data:
        # Prepare material data
        material_data = {
            "id": material_data.get('id'),
            "name": material_data.get('name'),
            "safety_stock": material_data.get('safety_stock'),
            "lot_size": material_data.get('lot_size'),
            "stock_level": material_data.get('stock_level')
        }
        
        # Check if ID is provided
        if 'id' in material_data:
            material = Material.query.get(material_data['id'])
            if not material:
                return jsonify({'error': f'Material with id {material_data["id"]} not found'}), 404
            # Update existing material
            for key, value in material_data.items():
                setattr(material, key, value)
        else:
            # Create new material
            material = Material(**material_data)
            db.session.add(material)

    db.session.commit()

    return jsonify({'message': 'Materials created/updated successfully'}), 200

###################################################
# Delete a single Material
###################################################
@material_bp.route('/<int:material_id>', methods=['DELETE'])
def delete_material(material_id):
    from app import db
    material = Material.query.get(material_id)
    if material:
        # Delete from the database
        MaterialsPerProduct.query.filter_by(MaterialsPerProduct.material_id==material_id).delete()
        
        MaterialsPerSupplier.query.filter_by(MaterialsPerSupplier.material_id==material_id).delete()
        
        Price.query.filter_by(Price.material_id == material_id).delete()
        
        db.session.delete(material)
        db.session.commit()
        return jsonify({'message': 'Material and associated records deleted successfully'}), 200
    else:
        return jsonify({'error': 'Material not found'}), 404