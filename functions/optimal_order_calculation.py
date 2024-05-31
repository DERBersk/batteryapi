import datetime
from collections import defaultdict
from models.base_production_volume import BaseProductionVolume
from models.project import Project
from models.material import Material
from models.products_per_project import ProductsPerProject
from models.materials_per_product import MaterialsPerProduct
from models.materials_per_supplier import MaterialsPerSupplier
from models.weekly_material_demand import WeeklyMaterialDemand

# File for Order Calculation Function
def MaterialDemandCalculation():
    # Fetch Base Production Data for each product with all weeks later than Current week, weekly basis
    base_volume_weekly = BaseProductionVolume.query.filter(is_later_or_equal((BaseProductionVolume.week,BaseProductionVolume.year))).all()
    
    # Fetch the Project Data, weekly basis (next month)
    product_per_projects = Project.query.filter(check_project_date(Project.start_date,Project.end_date)).join(ProductsPerProject).filter(Project.id==ProductsPerProject.project_id).add_columns(Project.id,Project.start_date,Project.end_date,ProductsPerProject.amount, ProductsPerProject.product_id).all()
    
    # Fetch Data for Product composition
    materials_per_products = MaterialsPerProduct.query.all()
    
    # Calculate weekly total Product demand (Sum of Demands)
    weekly_total = get_weekly_totals(base_volume_weekly, product_per_projects)
    
    # Calculate weekly total Material demand (Demand and Composition fit)
    material_demand_dict = calculate_material_demand(weekly_total,materials_per_products)
    
    # Save Data in new Table Material Demand (if Data already exists, update data)
    save_weekly_material_demand(material_demand_dict)

    return ""

def OptimalOrderCalculation():
    # Fetch weekly Material Demand Data
    weekly_material_demand = WeeklyMaterialDemand.query.all()
    
    # Fetch Lead times
    # TODO: Strategy involvement
    lead_times = MaterialsPerSupplier.query.filter(MaterialsPerSupplier.availability == True).add_columns(MaterialsPerSupplier.material_id,MaterialsPerSupplier.supplier_id,MaterialsPerSupplier.lead_time)
    
    # Fetch Safety Stock
    safety_stock = Material.query.add_columns(Material.id, Material.safety_stock).all()
    
    # If Inventory smaller than Safety Stock: Order needed anyway
    
    # Fetch Supplier for Material each after employed strategy
    
    # For each of the Materials
    
        # Aggregate Demanded Material in lead time (of Supplier) area (5 days lead time = Material Demand next 2 weeks (weeks rounded up +1))
    
        # If Demanded Material + Safety Stock is smaller than the inventory: Recommend no order
        
        # If Demanded Material + Safety Stock is bigger than the inventory: Recommend order
        
    # Return List of recommended orders
    
    return ""

def is_later_or_equal(week_year_tuple):
    """
    Compares a tuple (week, year) to the current week and year.
    
    Parameters:
    week_year_tuple (tuple): The tuple (week, year) to compare.
    
    Returns:
    bool: True if the input tuple is later than or equal to the current week and year, False otherwise.
    """
    current_year, current_week = datetime.now().isocalendar()[:2]
    
    input_week, input_year = week_year_tuple
    
    if input_year > current_year:
        return True
    elif input_year == current_year:
        return input_week >= current_week
    else:
        return False
    
def check_project_date(start_date, end_date, check_date=None):
    """
    Checks if a given date is within the start and end date range or if the project is incoming.
    
    Parameters:
    start_date (datetime): The start date of the project.
    end_date (datetime): The end date of the project.
    check_date (datetime, optional): The date to check. Defaults to the current date.
    
    Returns:
    Boolean: True if the project is incoming or current, false if it is past
    """
    if check_date is None:
        check_date = datetime.now()
    
    if check_date < start_date:
        return True
    elif start_date <= check_date <= end_date:
        return True
    else:
        return False
    
def get_weekly_totals(base_volume_weekly, product_per_projects):
    # Step 1: Aggregate base volumes by (product_id, year, week)
    base_volume_dict = defaultdict(float)
    for entry in base_volume_weekly:
        _, product_id, year, week, amount = entry
        base_volume_dict[(product_id, year, week)] += amount
    
    # Step 2: Distribute project amounts across weeks
    project_volume_dict = defaultdict(float)
    for entry in product_per_projects:
        _, product_id, start_date_str, end_date_str, amount = entry
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        days_in_project = (end_date - start_date).days + 1
        daily_amount = amount / days_in_project
        
        current_date = start_date
        while current_date <= end_date:
            year, week, _ = current_date.isocalendar()
            project_volume_dict[(product_id, year, week)] += daily_amount
            current_date += datetime.timedelta(days=1)
    
    # Step 3: Combine base volumes and project volumes
    total_volume_dict = defaultdict(float)
    for (product_id, year, week), amount in base_volume_dict.items():
        total_volume_dict[(product_id, year, week)] += amount
    
    for (product_id, year, week), amount in project_volume_dict.items():
        total_volume_dict[(product_id, year, week)] += amount
    
    # Convert defaultdict to regular dict for the result
    total_volume_dict = dict(total_volume_dict)
    
    return total_volume_dict

def calculate_material_demand(weekly_product_totals, materials_per_product):
    material_demand_dict = defaultdict(float)
    
    for (product_id, year, week), product_amount in weekly_product_totals.items():
        for material in materials_per_product:
            if material.product_id == product_id:
                material_demand_dict[(material.material_id, year, week)] += material.amount * product_amount
    
    # Convert defaultdict to regular dict for the result
    material_demand_dict = dict(material_demand_dict)
    
    return material_demand_dict

def save_weekly_material_demand(material_demand_dict):
    from extensions import db
    # Clear existing data (optional)
    db.session.query(WeeklyMaterialDemand).delete()

    # Add new data
    for (material_id, year, week), amount in material_demand_dict.items():
        weekly_demand = WeeklyMaterialDemand(
            material_id=material_id,
            year=year,
            week=week,
            amount=amount
        )
        db.session.add(weekly_demand)
    
    db.session.commit()
