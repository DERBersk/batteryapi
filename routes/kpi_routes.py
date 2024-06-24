# import external packages
from flask import Blueprint, jsonify
# import functions and data
from functions.risk_calculation import CountryRisk
from functions.optimal_order_calculation import MaterialDemandCalculation, OptimalOrderCalculation
from functions.reliability_calculation import ReliabilityCalculation
from functions.dashboard_calculations import CriticalSupplierCalculation, MaterialsWoSuppliersCalculation, OrderVolumeLastYearCalculation,IncomingOrderCalculation,MostProducedProduct

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
def CountryRiskGet():
    return jsonify(CountryRisk())

###################################################
# Route for the Return and Calculation
# of reliability
###################################################
@kpi_bp.route('/reliability', methods=['GET'])
def Reliability():
    ReliabilityCalculation()
    return jsonify('Computation Successful!')

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

###################################################
# Route for all critical Suppliers
# everyone below 0.5
###################################################
@kpi_bp.route('/criticalSuppliers', methods=['GET'])
def CriticalSuppliers():
    return jsonify(CriticalSupplierCalculation())

###################################################
# Route for all unsupplied Materials
###################################################
@kpi_bp.route('/materialWithoutSupplier', methods=['GET'])
def MaterialsWithoutSuppliers():
    return jsonify(MaterialsWoSuppliersCalculation())

###################################################
# Route for Order Volume for the past year
###################################################
@kpi_bp.route('/orderVolume', methods=['GET'])
def OrderVolumeGet():
    return jsonify(OrderVolumeLastYearCalculation())

###################################################
# Route for most produced product over last year
###################################################
@kpi_bp.route('/mostProduced', methods=['GET'])
def MostProducedGet():
    return jsonify(MostProducedProduct())

###################################################
# Route for incoming orders / incoming production
###################################################
@kpi_bp.route('/incomingOrders', methods=['GET'])
def IncomingOrdersGet():
    return jsonify(IncomingOrderCalculation())
