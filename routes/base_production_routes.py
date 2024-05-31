from flask import Blueprint, request, jsonify
from extensions import db
from models.base_production_volume import BaseProductionVolume

base_productionbp = Blueprint('baseproduction', __name__, url_prefix='/api/baseproduction')

# TODO: Documentation

###################################################
# Get for multiple base production volumes
###################################################
@base_productionbp.route('/', methods=['GET'])
def get_base_production_volumes():
    base_production_volumes = BaseProductionVolume.query.all()
    return jsonify([bpv.serialize() for bpv in base_production_volumes])

###################################################
# Post a single or multiple base production volumes
###################################################
@base_productionbp.route('/', methods=['POST'])
def post_base_production_volume():
    data = request.get_json()
    
    # Check if we have an id in the data to edit an existing record
    if 'id' in data:
        base_production_volume = BaseProductionVolume.query.get(data['id'])
        if not base_production_volume:
            return jsonify({'message': 'BaseProductionVolume not found'}), 404

        base_production_volume.product_id = data.get('product_id', base_production_volume.product_id)
        base_production_volume.year = data.get('year', base_production_volume.year)
        base_production_volume.week = data.get('week', base_production_volume.week)
        base_production_volume.amount = data.get('amount', base_production_volume.amount)
    else:
        base_production_volume = BaseProductionVolume(
            product_id=data['product_id'],
            year=data['year'],
            week=data['week'],
            amount=data['amount']
        )
        db.session.add(base_production_volume)
    
    db.session.commit()
    return jsonify(base_production_volume.serialize()), 201

###################################################
# Delete for single base production volume
###################################################
@base_productionbp.route('/<int:id>', methods=['DELETE'])
def delete_base_production_volume(id):
    base_production_volume = BaseProductionVolume.query.get(id)
    if not base_production_volume:
        return jsonify({'message': 'BaseProductionVolume not found'}), 404
    
    db.session.delete(base_production_volume)
    db.session.commit()
    return jsonify({'message': 'BaseProductionVolume deleted successfully'}), 200