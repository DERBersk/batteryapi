from collections import defaultdict
from models.base_production_volume import BaseProductionVolume
from models.project import Project
from models.material import Material
from models.supplier import Supplier
from models.options import StrategyEnum, Options
from models.week import Week
from models.price import Price
from models.products_per_project import ProductsPerProject
from models.materials_per_product import MaterialsPerProduct
from models.materials_per_supplier import MaterialsPerSupplier
from models.weekly_material_demand import WeeklyMaterialDemand

###############################################################################################
# Main Functions
###############################################################################################

# File for Order Calculation Function
def MaterialDemandCalculation():
    # Fetch Base Production Data for each product with all weeks later than Current week, weekly basis
    base_volume_weekly_all = BaseProductionVolume.query.all()
    
    filtered_base_volume = [record for record in base_volume_weekly_all if record.is_later_or_equal]
    
    # Fetch the Project Data, weekly basis (next month)
    product_per_projects_all = Project.query.join(ProductsPerProject).filter(Project.id==ProductsPerProject.project_id).add_columns(Project.id,Project.start_week,Project.end_week,ProductsPerProject.amount, ProductsPerProject.product_id).all()
    
    filtered_product_per_projects = [project for project in product_per_projects_all if project.Project.check_project_week()]
    
    # Fetch Data for Product composition
    materials_per_products = MaterialsPerProduct.query.all()
    
    # Calculate weekly total Product demand (Sum of Demands)
    weekly_total = get_weekly_totals(filtered_base_volume, filtered_product_per_projects)
    
    # Calculate weekly total Material demand (Demand and Composition fit)
    material_demand_dict = calculate_material_demand(weekly_total,materials_per_products)
    
    # Save Data in new Table Material Demand (if Data already exists, update data)
    save_weekly_material_demand(material_demand_dict)

    res = WeeklyMaterialDemand.query.all()

    return res

def OptimalOrderCalculation():
    # Fetch all necessary data before the loop
    materials = Material.query.all()
    options = Options.query.first()
    suppliers = Supplier.query.filter(Supplier.availability == True).all()
    prices = Price.query.filter(Price.end_date.is_(None)).all()
    materials_per_supplier = MaterialsPerSupplier.query.all()
    weekly_material_demands = WeeklyMaterialDemand.query.all()
    
    # Preprocess data for quick lookup
    supplier_dict = {supplier.id: supplier for supplier in suppliers}
    price_dict = {(price.supplier_id, price.material_id): price for price in prices}
    materials_per_supplier_dict = {(mps.supplier_id, mps.material_id): mps for mps in materials_per_supplier}
    weekly_material_demands_dict = {}
    for demand in weekly_material_demands:
        if demand.material_id not in weekly_material_demands_dict:
            weekly_material_demands_dict[demand.material_id] = []
        weekly_material_demands_dict[demand.material_id].append(demand)
    
    rec_order_list = []
    
    for material in materials:
        material_id = material.id
        order_needed = False
        strategy = material.strategy.value if material.strategy else options.strategy.value
        supplier = None
        
        if strategy == "Sustainability":
            supplier = max(
                [s for s in suppliers if (s.id, material_id) in materials_per_supplier_dict],
                key=lambda s: s.sustainability_index,
                default=None
            )
        elif strategy == "Risk":
            supplier = max(
                [s for s in suppliers if (s.id, material_id) in materials_per_supplier_dict],
                key=lambda s: s.risk_index,
                default=None
            )
        elif strategy == "Price":
            supplier = min(
                [p for p in prices if p.material_id == material_id],
                key=lambda p: p.cost,
                default=None
            )
            if supplier:
                supplier = supplier_dict[supplier.supplier_id]
        elif strategy == "LeadTime":
            supplier = min(
                [mps for mps in materials_per_supplier if mps.material_id == material_id],
                key=lambda mps: mps.lead_time,
                default=None
            )
            if supplier:
                supplier = supplier_dict[supplier.supplier_id]
        
        if not supplier:
            continue
        
        supplier_id = supplier.id
        price = price_dict.get((supplier_id, material_id))
        price = price.cost if price else None
        
        if not price:
            continue
        
        lead_time = materials_per_supplier_dict.get((supplier_id, material_id)).lead_time
        
        sustainability_index = supplier.sustainability_index
        risk_index = supplier.risk_index
        
        weekly_material_demand = weekly_material_demands_dict.get(material_id, [])
        filtered_weekly_material_demand = [record for record in weekly_material_demand if record.is_later_or_equal]
        
        lead_time_demand = get_lead_time_demand(filtered_weekly_material_demand, lead_time)
        
        total_demand = lead_time_demand + material.safety_stock
        if total_demand <= material.stock_level:
            order_needed = False
            min_order = 0
        else:
            order_needed = True
            min_order = total_demand - material.stock_level
        
        material_recommendation = {
            "material_id": material_id,
            "order_needed": order_needed,
            "strategy": strategy,
            "min_order": min_order,
            "supplier_id": supplier_id,
            "lead_time": lead_time,
            "sustainability_index": sustainability_index,
            "risk_index": risk_index,
            "price": price
        }
        rec_order_list.append(material_recommendation)
    
    return rec_order_list
    
###############################################################################################
# Support Functions
###############################################################################################
    
def get_weekly_totals(base_volume_weekly, product_per_projects):
    weeks = Week.query.all()
    week_mapping = {week.id: (int(week.year), int(week.week)) for week in weeks}
    # Step 1: Aggregate base volumes by (product_id, year, week)
    base_volume_dict = defaultdict(float)
    for entry in base_volume_weekly:
        product_id = entry.product_id
        year, week = week_mapping[entry.week_id]
        amount = entry.amount
        base_volume_dict[(product_id, year, week)] += amount
    

    # Step 2: Distribute project amounts across weeks
    project_volume_dict = defaultdict(float)
    # Iteriere durch alle Projekte
    for project in product_per_projects:
        start_week_id = project.start_week
        end_week_id = project.end_week
        product_id = project.product_id
        total_amount = project.amount

        # Hole die (year, week) Werte für Start- und Endwochen
        start_year, start_week = week_mapping[start_week_id]
        end_year, end_week = week_mapping[end_week_id]

        # Berechne die Anzahl der Wochen im Bereich von start_week bis end_week
        num_weeks = weeks_between(start_year, start_week, end_year, end_week)
        weekly_amount = total_amount / num_weeks

        # Iteriere durch alle Wochen im Bereich von start_week bis end_week und teile den Betrag auf
        current_year, current_week = start_year, start_week
        while (current_year < end_year) or (current_year == end_year and current_week <= end_week):
            project_volume_dict[(product_id, current_year, current_week)] = weekly_amount

            # Nächste Woche
            current_week += 1
            if current_week > 52:  # Annahme: 52 Wochen pro Jahr
                current_week = 1
                current_year += 1

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
        wk = Week.query.filter(Week.year == year).filter(Week.week == week).first()
        weekly_demand = WeeklyMaterialDemand(
            material_id=material_id,
            week_id=wk.id,
            amount=amount
        )
        db.session.add(weekly_demand)
    
    db.session.commit()
    
# Hilfsfunktion zur Berechnung der Anzahl der Wochen zwischen zwei Wochen
def weeks_between(start_year, start_week, end_year, end_week):
    total_weeks = 0
    current_year, current_week = start_year, start_week
    while (current_year < end_year) or (current_year == end_year and current_week <= end_week):
        total_weeks += 1
        current_week += 1
        if current_week > 52:  # Annahme: 52 Wochen pro Jahr
            current_week = 1
            current_year += 1
    return total_weeks

def get_lead_time_demand(weekly_material_demand, lead_time):
    total_demand = 0
    for demand in weekly_material_demand:
        if demand.is_in_lead_time(lead_time):
            total_demand += demand.amount
    return total_demand-1
        