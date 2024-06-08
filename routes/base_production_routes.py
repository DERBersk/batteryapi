# import external packages
from flask import Blueprint, request, jsonify
# import functions and data
from extensions import db
# import models
from models.base_production_volume import BaseProductionVolume

base_productionbp = Blueprint('baseproduction', __name__, url_prefix='/api/baseproduction')

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

    if not isinstance(data, list):
        return jsonify({'message': 'Data should be a list of base production volumes'}), 400

    for entry in data:
        if 'id' in entry:
            base_production_volume = BaseProductionVolume.query.get(entry['id'])
            if not base_production_volume:
                return jsonify({'message': f'BaseProductionVolume with id {entry["id"]} not found'}), 404

            base_production_volume.product_id = entry.get('product_id', base_production_volume.product_id)
            base_production_volume.week_id = entry.get('week_id', base_production_volume.week_id)
            base_production_volume.amount = entry.get('amount', base_production_volume.amount)
        else:
            base_production_volume = BaseProductionVolume(
                product_id=entry['product_id'],
                week_id=entry['week_id'],
                amount=entry['amount']
            )
            db.session.add(base_production_volume)
    
    db.session.commit()
    return jsonify({'message': 'Base production volumes added/updated successfully'}), 201

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