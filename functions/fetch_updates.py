import requests
import datetime

from extensions import db

from models.material import Material, UnitEnum, StrategyEnum
from models.order import Order
from models.supplier import Supplier

def fetch_api_data_materials():
    url = "https://secondaryapi-wms.vercel.app/material/"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def update_or_create_materials():
    api_data = fetch_api_data_materials()
    
    for item in api_data:
        # Find the material by external_id
        material = Material.query.filter(Material.external_id==item['id']).first()
        
        if material:
            # Update the existing material
            material.name = item['description']
            material.lot_size = item['lot_size']
            material.safety_stock = item['safety_stock']
            material.stock_level = item['stock_level']
            material.unit = item['unit'] if item['unit'] else UnitEnum.Pcs  # Assuming UnitEnum has a default unit
        else:
            # Create a new material
            new_material = Material(
                name=item['description'],
                external_id=item['id'],
                lot_size=item['lot_size'],
                safety_stock=item['safety_stock'],
                stock_level=item['stock_level'],
                unit=item['unit'] if item['unit'] else UnitEnum.Pcs,  # Assuming UnitEnum has a default unit
                strategy=StrategyEnum.NONE  # Assuming StrategyEnum.NONE is the default
            )
            db.session.add(new_material)
    
    # Commit the changes to the database
    db.session.commit()
    
    
def fetch_api_data_orders():
    url = "https://secondaryapi-wms.vercel.app/order/"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def update_or_create_orders(api_data):
    for item in api_data:
        # Find the material by external_id
        material = Material.query.filter(Material.external_id==item['material_id']).first()
        if not material:
            print(f"Material with external_id {item['material_id']} not found.")
            continue
        
        # Find the supplier by external_id
        supplier = Supplier.query.filter(Supplier.external_id==item['supplier_id']).first()
        if not supplier:
            print(f"Supplier with external_id {item['supplier_id']} not found.")
            continue

        # Find the order by external_id
        order = Order.query.filter(Order.external_id==item['id']).first()
        
        if order:
            # Update the existing order
            order.material_id = material.id
            order.supplier_id = supplier.id
            order.amount = item['amount']
            order.planned_delivery_date = datetime.datetime.strptime(item['planned_delivery_date'], '%a, %d %b %Y %H:%M:%S %Z')
            order.delivery_date = datetime.datetime.strptime(item['delivery_date'], '%a, %d %b %Y %H:%M:%S %Z')
        else:
            # Create a new order
            new_order = Order(
                external_id=item['id'],
                material_id=material.id,
                supplier_id=supplier.id,
                amount=item['amount'],
                planned_delivery_date=datetime.datetime.strptime(item['planned_delivery_date'], '%a, %d %b %Y %H:%M:%S %Z'),
                delivery_date=datetime.datetime.strptime(item['delivery_date'], '%a, %d %b %Y %H:%M:%S %Z')
            )
            db.session.add(new_order)
    
    # Commit the changes to the database
    db.session.commit()

