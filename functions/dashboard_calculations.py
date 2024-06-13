# import external packages
from datetime import datetime, timedelta
from collections import defaultdict
# import functions and data
from extensions import db
# import models
from models.supplier import Supplier
from models.material import Material
from models.materials_per_supplier import MaterialsPerSupplier
from models.order import Order
from models.base_production_volume import BaseProductionVolume
from models.project import Project
from models.product import Product
from models.products_per_project import ProductsPerProject

def CriticalSupplierCalculation():
    risky = Supplier.query.filter(Supplier.risk_index>0.5).all()
    unsustainable = Supplier.query.filter(Supplier.sustainability_index<0.5).all()
    unreliable = Supplier.query.filter(Supplier.reliability<0).all()
    
    res = {
        "risk": [risk.serialize() for risk in risky],
        "sustainability": [sus.serialize() for sus in unsustainable],
        "reliability": [rel.serialize() for rel in unreliable]
    }
    
    return res

def MaterialsWoSuppliersCalculation():
    materials_with_no_suppliers = Material.query.outerjoin(MaterialsPerSupplier, Material.id == MaterialsPerSupplier.material_id)\
                                                .filter(MaterialsPerSupplier.id == None)\
                                                .all()
    
    # Serialize the results
    result = [material.serialize() for material in materials_with_no_suppliers]
    
    return result

def OrderVolumeLastYearCalculation():
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    
    # Initialize a dictionary with all months in the past year with 0 volumes
    monthly_volumes = defaultdict(float)
    current_month = one_year_ago.replace(day=1)
    while current_month <= today:
        month_str = current_month.strftime('%Y-%m')
        monthly_volumes[month_str] = 0
        next_month = current_month.month % 12 + 1
        current_month = current_month.replace(month=next_month, year=current_month.year + (next_month == 1))
    
    # Fetch all relevant orders within the past year
    orders = db.session.query(
        Order.delivery_date,
        Order.amount
    ).filter(
        Order.delivery_date >= one_year_ago
    ).all()
    
    # Aggregate orders by month
    for order in orders:
        month = order.delivery_date.strftime('%Y-%m')
        monthly_volumes[month] += order.amount
    
    # Convert the result to a list of dictionaries
    result = [{'month': month, 'total_volume': total_volume} for month, total_volume in sorted(monthly_volumes.items())]
    
    return result

def IncomingOrderCalculation():
    today = datetime.now()
    
    # Query to fetch all incoming orders
    incoming_orders = db.session.query(Order).filter(Order.delivery_date > today).all()
    
    # Serialize the orders
    result = [order.serialize() for order in incoming_orders]
    
    return result

# File for Order Calculation Function
def MostProducedProduct():
    # Fetch Base Production Data for each product with all weeks later than Current week, weekly basis
    base_volume_weekly_all = BaseProductionVolume.query.all()
    
    filtered_base_volume = [record for record in base_volume_weekly_all if record.is_later_or_equal]
    
    # Fetch the Project Data, weekly basis (next month)
    product_per_projects_all = Project.query.join(ProductsPerProject).filter(Project.id==ProductsPerProject.project_id).add_columns(Project.id,Project.start_week,Project.end_week,ProductsPerProject.amount, ProductsPerProject.product_id).all()
    
    filtered_product_per_projects = [project for project in product_per_projects_all if project.Project.check_project_week_past_year()]
    
    res = get_highest_product_total(filtered_base_volume,filtered_product_per_projects)
    
    return res

def get_highest_product_total(base_volume_weekly, product_per_projects):
     # Step 1: Initialize a dictionary to store product totals
    product_totals = defaultdict(float)
    
    # Step 2: Aggregate base volumes by product_id
    for entry in base_volume_weekly:
        product_id = entry.product_id
        amount = entry.amount
        product_totals[product_id] += amount
    
    # Step 3: Distribute project amounts across products
    for project in product_per_projects:
        product_id = project.product_id
        total_amount = project.amount
        product_totals[product_id] += total_amount
    
    # Step 4: Find the product with the highest total amount
    max_product = None
    max_amount = 0.0
    
    for product_id, total_amount in product_totals.items():
        if total_amount > max_amount:
            max_amount = total_amount
            max_product = product_id
    
    product=Product.query.filter(Product.id==max_product).first()
    
    res = {
        "id":product.id,
        "description":product.description,
        "specification":product.specification,
        "amount":max_amount
    }
    
    # Return the product_id with the highest total amount
    return res
    
    