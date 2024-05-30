from flask import Blueprint, jsonify, request
from datetime import datetime
from functions.risk_calculation import load_country_data,transform_country_data

kpi_bp = Blueprint('kpi', __name__, url_prefix='/api/kpi')

### TODO: Documentation

###################################################
# Get for Sustainability Index
###################################################
@kpi_bp.route('/susindex', methods=['GET'])
def get_sus_index():
    return jsonify('Returns Sustainability Index!')

# Define the Flask route for the GET response
@kpi_bp.route('/countryrisk', methods=['GET'])
def get_transformed_countries():
    country_data = load_country_data()
    transformed_data = transform_country_data(country_data)
    return jsonify(transformed_data)
