# import external packages
import datetime
from flask import Blueprint, request, jsonify
# import functions and data
from extensions import db
# import models
from models.order import Order

order_bp = Blueprint('order', __name__, url_prefix='/api/order')

###################################################
# Get for multiple orders
###################################################
@order_bp.route('/', methods=['GET'])
def get_order():
    orders = Order.query.all()
    return jsonify([order.serialize() for order in orders])

###################################################
# Post a single or multiple orders
###################################################
@order_bp.route('/', methods=['POST'])
def post_orders():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'message': 'Data should be a list of orders'}), 400

    for entry in data:
        if 'id' in entry:
            order = Order.query.get(entry['id'])
            if not order:
                return jsonify({'message': f'Order with id {entry["id"]} not found'}), 404

            order.material_id = entry.get('material_id', order.material_id)
            order.supplier_id = entry.get('supplier_id', order.supplier_id)
            order.amount = entry.get('amount', order.amount)
            order.planned_delivery_date = datetime.datetime.strptime(entry.get('plannded_delivery_date'),'%m-%d-%y').date()
            order.delivery_date = datetime.datetime.strptime(entry.get('delivery_date'),'%m-%d-%y').date()
        else:
            order = Order(
                material_id=entry['material_id'],
                supplier_id=entry['supplier_id'],
                amount=entry['amount'],
                planned_delivery_date=datetime.datetime.strptime(entry['planned_delivery_date'],'%m-%d-%y').date(),
                delivery_date=datetime.datetime.strptime(entry['delivery_date'],'%m-%d-%y').date()
            )
            db.session.add(order)
    
    db.session.commit()
    return jsonify({'message': 'orders added/updated successfully'}), 201

###################################################
# Delete for single order
###################################################
@order_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200