import requests
import datetime
from collections import defaultdict
from sqlalchemy.exc import IntegrityError

from extensions import db

from models.material import Material, UnitEnum, StrategyEnum
from models.order import Order
from models.supplier import Supplier
from models.external_production_data import ExternalProductionData
from models.product import Product

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

def update_or_create_orders():
    api_data = fetch_api_data_orders()
    
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
    
    orders = Order.query.all()
    return [order.serialize() for order in orders]

def fetch_api_data_production_volume():
    url = "https://secondaryapi-mes.vercel.app/productionvolume/"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def get_week_id_from_date(date):
    week_number = date.strftime("%U")
    year = date.strftime("%Y")
    return f"wk{week_number}_{year}"

def update_or_create_production_volume():
    api_data = fetch_api_data_production_volume()
    
    products = Product.query.all()
    
    # Create a dictionary to map external_id to product_id
    product_map = {product.external_id: product.id for product in products}
    
    # Group data by product_id and week_id and cumulate the amounts
    grouped_data = defaultdict(float)
    
    for item in api_data:
        date = datetime.datetime.strptime(item['date'], "%a, %d %b %Y %H:%M:%S %Z")
        week_id = get_week_id_from_date(date)
        external_id = item['id']  # Assuming 'id' is the field for the external API ID
        amount = item['amount']
        product_id = item['product_id']
        
        product_id = product_map.get(product_id)
        
        if product_id:
            grouped_data[(product_id, week_id)] += amount

    # Iterate over the grouped data and update/create database records
    for (product_id, week_id), amount in grouped_data.items():
        # Check if the record already exists
        existing_record = ExternalProductionData.query.filter(
            ExternalProductionData.product_id == product_id,
            ExternalProductionData.week_id == week_id
        ).first()
        
        if existing_record:
            # Update the existing record
            existing_record.amount = amount
        else:
            # Create a new record
            new_record = ExternalProductionData(
                product_id=product_id,
                week_id=week_id,
                amount=amount,
                external_id=external_id  # Store the external API ID
            )
            db.session.add(new_record)
        
    # Commit the changes to the database
    try:
        db.session.commit()
        return "Data Update Successful!"
    except IntegrityError as e:
        db.session.rollback()
        print(f"An error occurred while committing the transaction: {e}")
    
