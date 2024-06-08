# import external packages
from flask import Blueprint, jsonify
# import functions and data
from functions.risk_calculation import load_country_data,transform_country_data
from functions.optimal_order_calculation import MaterialDemandCalculation, OptimalOrderCalculation

kpi_bp = Blueprint('kpi', __name__, url_prefix='/api/kpi')

###################################################
# Get for Sustainability Index
###################################################
@kpi_bp.route('/susindex', methods=['GET'])
def get_sus_index():
    return jsonify('Returns Sustainability Index!')

###################################################
# Get Risk of each Country
###################################################
@kpi_bp.route('/countryrisk', methods=['GET'])
def get_transformed_countries():
    country_data = load_country_data()
    transformed_data = transform_country_data(country_data)
    return jsonify(transformed_data)

###################################################
# Route for the Return and Calculation
# of weekly material demand
###################################################
@kpi_bp.route('/materialDemand', methods=['GET'])
def calculateWeeklyDemand():
    res = MaterialDemandCalculation()
    return jsonify([mdc.serialize() for mdc in res])

###################################################
# Route for the Return and Calculation
# of optimal orders
###################################################
@kpi_bp.route('/optimalOrders', methods=['GET'])
def OptimalOrders():
    return jsonify(OptimalOrderCalculation())