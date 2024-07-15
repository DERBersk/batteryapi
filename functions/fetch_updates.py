# import external packages
import requests
import datetime
from collections import defaultdict
from sqlalchemy.exc import IntegrityError
# import functions and data
from extensions import db
# import models
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
    
    # Fetch all materials and create a dictionary with external_id as the key
    existing_materials = {material.external_id: material for material in Material.query.all()}
    
    for item in api_data:
        # Define a dictionary to map the database fields to the API data
        material_data = {
            'name': item['description'],
            'lot_size': item['lot_size'],
            'safety_stock': item['safety_stock'],
            'stock_level': item['stock_level'],
            'unit': item['unit'] if item['unit'] else UnitEnum.Pcs  # Assuming UnitEnum has a default unit
        }
        
        # Check if the material exists in the existing materials dictionary
        material = existing_materials.get(item['id'])
        
        if material:
            # Update the existing material
            for key, value in material_data.items():
                setattr(material, key, value)
        else:
            # Create a new material
            material_data['external_id'] = item['id']
            material_data['strategy'] = StrategyEnum.NONE  # Assuming StrategyEnum.NONE is the default
            new_material = Material(**material_data)
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
    
    # Fetch all necessary data in a single query and store them in dictionaries
    existing_materials = {material.external_id: material for material in Material.query.all()}
    existing_suppliers = {supplier.external_id: supplier for supplier in Supplier.query.all()}
    existing_orders = {order.external_id: order for order in Order.query.all()}
    
    for item in api_data:
        # Check if the material exists in the existing materials dictionary
        material = existing_materials.get(item['material_id'])
        if not material:
            print(f"Material with external_id {item['material_id']} not found.")
            continue
        
        # Check if the supplier exists in the existing suppliers dictionary
        supplier = existing_suppliers.get(item['supplier_id'])
        if not supplier:
            print(f"Supplier with external_id {item['supplier_id']} not found.")
            continue
        
        # Check if the order exists in the existing orders dictionary
        order = existing_orders.get(item['id'])
        
        planned_delivery_date = datetime.datetime.strptime(item['planned_delivery_date'], '%a, %d %b %Y %H:%M:%S %Z')
        delivery_date = datetime.datetime.strptime(item['delivery_date'], '%a, %d %b %Y %H:%M:%S %Z') if item['delivery_date'] else None

        if order:
            # Update the existing order
            order.material_id = material.id
            order.supplier_id = supplier.id
            order.amount = item['amount']
            order.planned_delivery_date = planned_delivery_date
            order.delivery_date = delivery_date
        else:
            # Create a new order
            new_order = Order(
                external_id=item['id'],
                material_id=material.id,
                supplier_id=supplier.id,
                amount=item['amount'],
                planned_delivery_date=planned_delivery_date,
                delivery_date=delivery_date
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
    
