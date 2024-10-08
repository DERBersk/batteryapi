# import external packages
from flask import Blueprint, jsonify
# import functions and data
from functions.risk_calculation import CountryRisk, update_supplier_risk_indices
from functions.sustainability_calculations import calculate_sustainability_index
from functions.optimal_order_calculation import MaterialDemandCalculation, OptimalOrderCalculation, OptimalOrderCalculationOneWeek,MaterialDemand5Weeks, ProductDemand5Weeks
from functions.reliability_calculation import ReliabilityCalculation
from functions.dashboard_calculations import ProductDemandCalculation, CriticalSupplierCalculation, MaterialsWoSuppliersCalculation, OrderVolumeLastYearCalculation,IncomingOrderCalculation,MostProducedProduct,get_products_without_material, get_materials_per_supplier_without_price


kpi_bp = Blueprint('kpi', __name__, url_prefix='/api/kpi')

###################################################
# Get for Sustainability Index
###################################################
@kpi_bp.route('/susindex', methods=['GET'])
def get_sus_index():
    return jsonify(calculate_sustainability_index())

###################################################
# Get for Risk Index
###################################################
@kpi_bp.route('/riskindex', methods=['GET'])
def get_risk_index():
    return jsonify(update_supplier_risk_indices())

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
# Route for Return of the material Demand over the
# next 5 Weeks
###################################################
@kpi_bp.route('/materialDemand5Weeks', methods=['GET'])
def calculateWeeklyDemand5Weeks():
    res = MaterialDemand5Weeks()
    return jsonify(res)

###################################################
# Route for Return of the product Demand over the
# next 5 Weeks
###################################################
@kpi_bp.route('/productDemand5Weeks', methods=['GET'])
def calculateProductWeeklyDemand5Weeks():
    res = ProductDemand5Weeks()
    return jsonify(res)

###################################################
# Route for the Return and Calculation
# of optimal orders for the next 5 weeks
###################################################
@kpi_bp.route('/optimalOrders', methods=['GET'])
def OptimalOrders():
    return jsonify(OptimalOrderCalculation())

###################################################
# Route for the Return and Calculation
# of for this week
###################################################
@kpi_bp.route('/optimalOrdersOneWeek', methods=['GET'])
def OptimalOrdersOneWeek():
    return jsonify(OptimalOrderCalculationOneWeek())

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

###################################################
# Route for upcoming Productions
###################################################
@kpi_bp.route('/production', methods=['GET'])
def ProductionGet():
    return jsonify(ProductDemandCalculation())

###################################################
# Route for Products without compositions
###################################################
@kpi_bp.route('/productsWithoutMaterials', methods=['GET'])
def ProductWithoutMaterialGet():
    return jsonify(get_products_without_material())

###################################################
# Route for MaterialPerSupplier without Price
###################################################
@kpi_bp.route('/MaterialPerSupplierWithoutPrice', methods=['GET'])
def MaterialPerSupplierWithoutPriceGet():
    return jsonify(get_materials_per_supplier_without_price())