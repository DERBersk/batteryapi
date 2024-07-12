# import external packages
from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import case, func, and_
import requests
# import functions and data
from extensions import db
# import models
from models.supplier import Supplier
from models.material import Material
from models.materials_per_supplier import MaterialsPerSupplier
from models.price import Price
from models.order import Order

supplier_bp = Blueprint('supplier', __name__, url_prefix='/api/supplier')

def fetch_api_data_suppliers():
    url = "https://secondaryapi-wms.vercel.app/supplier/"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

###################################################
# Get for external Suppliers
###################################################
@supplier_bp.route('/external/', methods=['GET'])
def get_external_suppliers():
    api_data = fetch_api_data_suppliers()
    return jsonify(api_data)
    
###################################################
# Get for multiple Suppliers
###################################################
@supplier_bp.route('/', methods=['GET'])
def get_suppliers():
    # Get the filter parameters from the request
    material_ids = request.args.getlist('material_ids', type=int)

    # Step 1: Count materials per supplier
    mat_counts_query = db.session.query(
        Supplier.id,
        func.count(Material.id).label('mat_count')
    ).outerjoin(MaterialsPerSupplier, Supplier.id == MaterialsPerSupplier.supplier_id) \
    .outerjoin(Material, Material.id == MaterialsPerSupplier.material_id) \
    .group_by(Supplier.id) \
    .order_by(Supplier.id.asc())

    mat_counts = mat_counts_query.subquery()

    # Step 2: Count open orders (delivery_date is None) per supplier
    open_order_counts_query = db.session.query(
        Supplier.id,
        func.count(Order.id).filter(Order.delivery_date.is_(None)).label('open_order_count')
    ).outerjoin(Order, Order.supplier_id == Supplier.id) \
    .filter(Order.delivery_date.is_(None)) \
    .group_by(Supplier.id) \
    .order_by(Supplier.id.asc())

    open_order_counts = open_order_counts_query.subquery()

    # Final query joining all counts and filtering by material IDs if provided
    suppliers_query = db.session.query(
        Supplier,
        mat_counts.c.mat_count,
        open_order_counts.c.open_order_count
    ).outerjoin(mat_counts, mat_counts.c.id == Supplier.id) \
    .outerjoin(open_order_counts, open_order_counts.c.id == Supplier.id) \
    .outerjoin(MaterialsPerSupplier, Supplier.id == MaterialsPerSupplier.supplier_id) \
    .outerjoin(Material, Material.id == MaterialsPerSupplier.material_id)

    if material_ids:
        suppliers_query = suppliers_query.filter(Material.id.in_(material_ids))

    suppliers_query = suppliers_query.group_by(Supplier.id, mat_counts.c.mat_count, open_order_counts.c.open_order_count) \
                                     .order_by(Supplier.id.asc())

    # Fetch results and prepare data
    suppliers_data = []
    for supplier, mat_count, open_order_count in suppliers_query:
        supplier_data = supplier.serialize()
        supplier_data['mat_count'] = mat_count
        supplier_data['order_count'] = open_order_count
        suppliers_data.append(supplier_data)

    return jsonify(suppliers_data)
###################################################
# Get for a single Suppliers (inc. Material Data)
###################################################
@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.filter(Supplier.id == supplier_id).first()
    if supplier:
        materials = Material.query.join(MaterialsPerSupplier)\
                                  .join(Supplier)\
                                  .filter(MaterialsPerSupplier.supplier_id==supplier_id)\
                                  .filter(Material.id==MaterialsPerSupplier.material_id)\
                                  .add_columns(Material.id,Material.name,Material.safety_stock,Material.lot_size,Material.stock_level,MaterialsPerSupplier.lead_time, Material.unit, Material.external_id,MaterialsPerSupplier.co2_emissions,MaterialsPerSupplier.distance)\
                                  .order_by(Material.id.asc())\
                                  .all()
        materials_list = []
        for material in materials:
            price = Price.query.filter(Price.supplier_id == supplier_id)\
                           .filter(Price.end_date is not None)\
                           .filter(Price.material_id == material.id)\
                           .order_by(Price.cost).first()
            price_val = 0
            if price:
                price_val = price.cost
            
            materials_list.append(
                {
                    'id': material.id,
                    'name': material.name,
                    'safety_stock': material.safety_stock,
                    'lot_size': material.lot_size,
                    'stock_level': material.stock_level,
                    'lead_time': material.lead_time,
                    'unit': material.unit.name if material.unit else None,
                    'price': price_val,
                    'external_id': material.external_id,
                    'co2_emissions': material.co2_emissions,
                    'distance': material.distance
                }
            )
            
        orders = Order.query.filter(Order.delivery_date.is_(None)).filter(Order.supplier_id == supplier_id).order_by(Order.id).all()
        order_list = []
        for order in orders:
            
            order_list.append(
                {
                    'id': order.id,
                    'material_id': order.material_id,
                    'supplier_id': order.supplier_id,
                    'amount': order.amount,
                    'planned_delivery_date': order.planned_delivery_date,
                    'delivery_date': order.delivery_date,
                    'external_id': order.external_id,
                }
            )
            
        supplier_data = {
                'id': supplier.id,
                'name': supplier.name,
                'lat': supplier.lat,
                'long': supplier.long,
                'risk_index': supplier.risk_index,
                'sustainability_index':supplier.sustainability_index,
                'reliability':supplier.reliability,
                'availability':supplier.availability,
                'country': supplier.country,
                'email': supplier.email,
                'external_id': supplier.external_id,
                'materials': materials_list,
                'open_orders': order_list
        }
        return jsonify(supplier_data), 200
    else:
        return jsonify({'message': f'Supplier with id {supplier_id} not found'}), 404

###################################################
# Post a single or multiple suppliers
###################################################
@supplier_bp.route('', methods=['POST'])
def create_or_update_suppliers():
    from app import db
    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format. Expected a list of suppliers.'}), 400

    for supplier_data in data:
        # Create or update supplier
        if 'id' in supplier_data and supplier_data.get('id') != None:
            supplier = Supplier.query.get(supplier_data['id'])
            if not supplier:
                return jsonify({'message': f'Supplier with id {supplier_data["id"]} not found'}), 404
            for key, value in supplier_data.items():
                if key != 'id' and key != 'materials':
                    setattr(supplier, key, value)
        else:
            supplier_data['availability'] = (supplier_data.get('availability') == "True") | (supplier_data.get('availability') == "true")
            supplier = Supplier(**{k: v for k, v in supplier_data.items() if k != 'materials'})

        db.session.add(supplier)

        # Extract materials data
        materials_data = supplier_data.get('materials', [])
        MaterialsPerSupplier.query.filter(MaterialsPerSupplier.supplier_id == supplier.id).delete()
        for material_data in materials_data:
            material_id = material_data.get('id')
            if material_id:
                material = Material.query.get(material_id)
                if not material:
                    return jsonify({'message': f'Material with id {material_id} not found'}), 404

            # Add or update MaterialsPerSupplier
            lead_time = material_data.get('lead_time')
            co2_emissions = material_data.get('co2_emissions')
            distance = material_data.get('distance')
            
            new_price = material_data.get('price')
            
            cur_price = Price.query.filter(
                Price.supplier_id == supplier.id,
                Price.material_id == material_id,
                Price.end_date.is_(None)
            ).first()
            
            if cur_price:
                if cur_price.cost != new_price:
                    cur_price.end_date = datetime.today().date() 
                    db.session.commit()
                    price = Price(
                        supplier_id=supplier.id,
                        material_id=material_id,
                        cost = new_price,
                        start_date = datetime.today().date()     
                    )
                    db.session.add(price)
            else:
                price = Price(
                    supplier_id=supplier.id,
                    material_id=material_id,
                    cost = new_price,
                    start_date = datetime.today().date()     
                )
                db.session.add(price)

            materials_per_supplier = MaterialsPerSupplier(
                supplier_id=supplier.id,
                material_id=material.id,
                lead_time=lead_time,
                co2_emissions=co2_emissions,
                distance=distance
            )
            db.session.add(materials_per_supplier)

    db.session.commit()
    
    # Subquery to get all material_id and supplier_id combinations from MaterialPerSupplier
    subquery = db.session.query(
        MaterialsPerSupplier.material_id,
        MaterialsPerSupplier.supplier_id
    ).subquery()

    # Delete all Price entries that do not have a corresponding MaterialPerSupplier entry
    db.session.query(Price).filter(
        ~and_(
            Price.material_id == subquery.c.material_id,
            Price.supplier_id == subquery.c.supplier_id
        )
    ).delete(synchronize_session='fetch')

    return jsonify({'message': 'Suppliers created/updated successfully'}), 200


###################################################
# Delete a single supplier
###################################################
@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    from app import db
    supplier = Supplier.query.get(supplier_id)
    if supplier:
        # Delete from the database
        MaterialsPerSupplier.query.filter_by(supplier_id = supplier_id).delete()
        
        Price.query.filter_by(supplier_id = supplier_id).delete()
        
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message': 'Supplier and associated records deleted successfully'}), 200
    else:
        return jsonify({'error': 'Supplier not found'}), 404
    
###################################################
# Get for a single Suppliers based on Material id
# (inc. Material Data)
###################################################
@supplier_bp.route('/material/<int:material_id>', methods=['GET'])
def get_supplier_on_material_id(material_id):
    supplier_per_material = []
    
    materials = MaterialsPerSupplier.query.join(Material).\
                                        filter(Material.id == MaterialsPerSupplier.material_id).\
                                        join(Supplier).\
                                        filter(Supplier.id == MaterialsPerSupplier.supplier_id).\
                                        filter(Material.id == material_id).\
                                        add_columns(MaterialsPerSupplier.material_id,Material.unit,Material.lot_size,Material.stock_level,Material.strategy,MaterialsPerSupplier.lead_time,MaterialsPerSupplier.co2_emissions,Supplier.availability,Supplier.id,Supplier.name,Supplier.country,Supplier.email,Supplier.lat,Supplier.long,Supplier.reliability,Supplier.sustainability_index,Supplier.risk_index).\
                                        all()
    
    for material in materials:
        material_json = {
            'supplier_id': material.id,
            'material_id': material.material_id,
            'supplier_name': material.name,
            'supplier_lat': material.lat,
            'supplier_long': material.long,
            'supplier_risk_index': material.risk_index,
            'supplier_reliability': material.reliability,
            'supplier_sustainability_index': material.sustainability_index,
            'supplier_availability': material.availability,
            'supplier_country': material.country,
            'mPs_lead_time': material.lead_time,
            'mPs_co2emissions': material.co2_emissions
        }
        supplier_per_material.append(material_json)
    
    return jsonify(supplier_per_material)