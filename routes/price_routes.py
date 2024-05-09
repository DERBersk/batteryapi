from flask import Blueprint, jsonify, request
from models.price import Price
from datetime import datetime

price_bp = Blueprint('price', __name__, url_prefix='/api/price')

###################################################
# Get for multiple prices
###################################################
@price_bp.route('/', methods=['GET'])
def get_prices():
    prices = Price.query.all()
    return jsonify([price.serialize() for price in prices])

###################################################
# Get for a single current Materialprice
###################################################
@price_bp.route('/<int:material_id>', methods=['GET'])
def get_material(material_id):
    price = Price.query.filter(Price.material_id == material_id)\
                       .filter(Price.end_date == "")\
                       .order_by(Price.cost).first()
    if price:
        return jsonify(price.serialize())
    else:
        return jsonify({'message': f'Price with material_id {material_id} and empty end_date not found'}), 404

###################################################
# Post a single or multiple prices
###################################################
@price_bp.route('/', methods=['POST'])
def create_or_update_prices():
    data = request.json
    from app import db
    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format. Expected a list of prices.'}), 400

    for price_data in data:
        
        price_data={
            "material_id":price_data.get('material_id'),
            "supplier_id":price_data.get('supplier_id'),
            "cost":price_data.get('cost'),
            "unit":price_data.get('unit'),
            "start_date":datetime.strptime(price_data.get('start_date'), "%Y-%m-%d"),
            "end_date":datetime.strptime(price_data.get('end_date'), "%Y-%m-%d")
        }
        
        if 'id' in price_data:
            product = Price.query.get(price_data['id'])
            if not product:
                return jsonify({'message': f'Price with id {price_data["id"]} not found'}), 404
            for key, value in price_data.items():
                setattr(product, key, value)
        else:
            price = Price(**price_data)

        db.session.add(price)
        

    db.session.commit()

    return jsonify({'message': 'Prices created successfully'}), 200

###################################################
# Delete a single price
###################################################
@price_bp.route('/<int:price_id>', methods=['DELETE'])
def delete_price(price_id):
    from app import db
    price = Price.query.get(price_id)
    if price:
        db.session.delete(price)
        db.session.commit()
        return jsonify({'message': 'Price deleted successfully'}), 200
    else:
        return jsonify({'error': 'Price not found'}), 404
