# import external packages
from flask import Blueprint, request, jsonify
# import functions and data
from functions.fetch_updates import update_or_create_production_volume
# import models
from models.external_production_data import ExternalProductionData

external_production_bp = Blueprint('externalproduction', __name__, url_prefix='/api/externalproduction')

###################################################
# Get for multiple base production volumes
###################################################
@external_production_bp.route('/', methods=['GET'])
def get_external_production_data():
    external_production_data = ExternalProductionData.query.all()
    return jsonify([epd.serialize() for epd in external_production_data])

###################################################
# Post a single or multiple base production volumes
###################################################
@external_production_bp.route('/', methods=['POST'])
def update_external_production_data():
    return jsonify(update_or_create_production_volume())
    