# import external packages
from collections import defaultdict
import json
# import functions and data
from extensions import db
# import models
from models.order import Order
from models.supplier import Supplier

with open('config.json', 'r') as file:
    config = json.load(file)

def ReliabilityCalculation():
    # Set threshold for supplier deliveries
    threshold = config['RELIABILITY_THRESHOLD']
    
    # Initialize a dictionary to store punctual deliveries and total deliveries per supplier
    supplier_data = defaultdict(lambda: {'punctual_deliveries': 0, 'total_deliveries': 0})
    
    # Fetch all orders at once
    orders = Order.query.all()
    
    for order in orders:
        supplier_id = order.supplier_id
        supplier_data[supplier_id]['total_deliveries'] += 1
        if order.is_punctual():
            supplier_data[supplier_id]['punctual_deliveries'] += 1
    
    # Fetch all suppliers
    suppliers = Supplier.query.all()
    
    for supplier in suppliers:
        if supplier.id in supplier_data:
            data = supplier_data[supplier.id]
            reliability = data['punctual_deliveries'] / data['total_deliveries']
            supplier.reliability = reliability - threshold
        else:
            supplier.reliability = None  # No orders found for this supplier
    
    # Commit changes to the database
    db.session.commit()