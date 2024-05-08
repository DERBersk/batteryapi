from flask import Blueprint, jsonify, request
import functions.create_test_data as cd

test_data_bp = Blueprint('createdata', __name__, url_prefix='/api/createdata')

###################################################
# Create Test data initially
###################################################
@test_data_bp.route('/', methods=['GET'])
def createData():
    cd.populate_suppliers()
    cd.populate_products()
    cd.populate_materials()
    cd.populate_projects()
    cd.populate_prices()
    cd.populate_demands()
    cd.populate_materials_per_supplier()
    cd.populate_materials_per_product()
    cd.populate_products_per_project()
    return jsonify('Creation successful!')