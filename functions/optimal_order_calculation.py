# import external packages
from collections import defaultdict
from datetime import date, timedelta, datetime
# import models
from models.external_production_data import ExternalProductionData
from models.project import Project
from models.material import Material
from models.supplier import Supplier
from models.options import Options
from models.week import Week
from models.price import Price
from models.products_per_project import ProductsPerProject
from models.materials_per_product import MaterialsPerProduct
from models.materials_per_supplier import MaterialsPerSupplier
from models.weekly_material_demand import WeeklyMaterialDemand
from models.product import Product
from models.order import Order

###############################################################################################
# Main Functions
###############################################################################################

# File for Order Calculation Function
def MaterialDemandCalculation():
    # Fetch Base Production Data for each product with all weeks later than Current week, weekly basis
    external_production_data = ExternalProductionData.query.all()
    
    filtered_external_production_data = [record for record in external_production_data if record.is_later_or_equal]
    
    # Fetch the Project Data, weekly basis (next month)
    product_per_projects_all = Project.query.join(ProductsPerProject).filter(Project.id==ProductsPerProject.project_id).add_columns(Project.id,Project.start_week,Project.end_week,ProductsPerProject.amount, ProductsPerProject.product_id).all()
    
    filtered_product_per_projects = [project for project in product_per_projects_all if project.Project.check_project_week()]
    
    # Fetch Data for Product composition
    materials_per_products = MaterialsPerProduct.query.all()
    
    # Calculate weekly total Product demand (Sum of Demands)
    weekly_total = get_weekly_totals(filtered_external_production_data, filtered_product_per_projects)
    
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
    prices = Price.query.filter(Price.end_date.is_(None)).join(Supplier).filter(Supplier.id == Price.supplier_id).filter(Supplier.availability == True).all()
    materials_per_supplier = MaterialsPerSupplier.query.join(Supplier).filter(Supplier.id == MaterialsPerSupplier.supplier_id).filter(Supplier.availability == True).all()
    weekly_material_demands = WeeklyMaterialDemand.query.all()
    outstanding_orders = Order.query.filter(Order.delivery_date.is_(None)).join(Supplier).filter(Supplier.id == Order.supplier_id).filter(Supplier.availability == True).all()
    weeks = Week.query.all()

    # Preprocess data for quick lookup
    supplier_dict = {supplier.id: supplier for supplier in suppliers}
    price_dict = {(price.supplier_id, price.material_id): price for price in prices}
    materials_per_supplier_dict = {(mps.supplier_id, mps.material_id): mps for mps in materials_per_supplier}
    weekly_material_demands_dict = {}
    for demand in weekly_material_demands:
        if demand.material_id not in weekly_material_demands_dict:
            weekly_material_demands_dict[demand.material_id] = []
        weekly_material_demands_dict[demand.material_id].append(demand)
    outstanding_orders_dict = {}
    for order in outstanding_orders:
        if order.material_id not in outstanding_orders_dict:
            outstanding_orders_dict[order.material_id] = []
        outstanding_orders_dict[order.material_id].append(order)
    
    week_dict = {f"wk{week.week}_{week.year}": week for week in weeks}
    
    rec_order_dict = {}

    today = date.today()
    
    for material in materials:
        material_id = material.id
        unit = material.unit.name if material.unit else None
        name = material.name
        strategy = material.strategy.value if material.strategy else options.strategy.value
        supplier = None
        
        if strategy == "Sustainability":
            valid_suppliers = [s for s in suppliers if (s.id, material_id) in materials_per_supplier_dict and s.sustainability_index is not None]
            if valid_suppliers:
                supplier = max(valid_suppliers, key=lambda s: s.sustainability_index)
            else:   
                continue
        elif strategy == "Risk":
            valid_suppliers = [s for s in suppliers if (s.id, material_id) in materials_per_supplier_dict and s.risk_index is not None]
            if valid_suppliers:
                supplier = max(valid_suppliers, key=lambda s: s.risk_index)
            else:
                continue
        elif strategy == "Price":
            valid_prices = [p for p in prices if p.material_id == material_id and p.cost is not None]
            if valid_prices:
                cheapest_price = min(valid_prices, key=lambda p: p.cost)
                supplier = supplier_dict[cheapest_price.supplier_id]
            else:
                continue
        elif strategy == "LeadTime":
            valid_materials = [mps for mps in materials_per_supplier if mps.material_id == material_id and mps.lead_time is not None]
            if valid_materials:
                shortest_lead_time = min(valid_materials, key=lambda mps: mps.lead_time)
                supplier = supplier_dict[shortest_lead_time.supplier_id]
            else:
                continue
        
        if not supplier:
            continue
        
        lt = materials_per_supplier_dict[(supplier.id, material_id)]
        
        if not lt.lead_time:
            continue
        
        supplier_id = supplier.id
        price = price_dict.get((supplier_id, material_id))
        price = price.cost if price else None
        
        if not price:
            continue
        
        mps = materials_per_supplier_dict.get((supplier_id, material_id))
        lead_time = mps.lead_time
        co2_emissions = mps.co2_emissions
        
        sustainability_index = supplier.sustainability_index
        risk_index = supplier.risk_index
        
        weekly_material_demand = weekly_material_demands_dict.get(material_id, [])
        filtered_weekly_material_demand = [record for record in weekly_material_demand if record.is_later_or_equal]
        
        for week in range(5):
            week_start = today + timedelta(weeks=week)
            week_number = week_start.isocalendar()[1]
            year = week_start.isocalendar()[0]
            week_key = f"wk{week_number}_{year}"

            lead_time_demand = get_lead_time_demand(filtered_weekly_material_demand, lead_time, week_start)
                        
            # Calculate total outstanding orders for the material within the lead time
            total_outstanding_orders = 0
            if material_id in outstanding_orders_dict:
                for order in outstanding_orders_dict[material_id]:
                    if is_within_lead_time(order.planned_delivery_date, lead_time, week_start):
                        total_outstanding_orders += order.amount
            total_demand = lead_time_demand + material.safety_stock - total_outstanding_orders
            
            if total_demand <= material.stock_level:
                continue
            else:
                min_order = total_demand - material.stock_level
                material_recommendation = {
                    "material_id": material_id,
                    "unit": unit,
                    "name": name,
                    "strategy": strategy,
                    "min_order": min_order,
                    "supplier_id": supplier_id,
                    "supplier_name": supplier.name,
                    "lead_time": lead_time,
                    "sustainability_index": sustainability_index,
                    "co2_emissions": co2_emissions,
                    "risk_index": risk_index,
                    "price": price,
                }
                if week_key not in rec_order_dict:
                    rec_order_dict[week_key] = []
                    
                if is_new_material(rec_order_dict,material_id):
                    rec_order_dict[week_key].append(material_recommendation)
        new_rec_order_list = []
        for week_key in rec_order_dict:
            wk = week_dict.get(week_key)
            new_rec_order_list.append({"week": wk.week, "year": wk.year, "data": rec_order_dict[week_key]})
        
        sorted_data = sorted(new_rec_order_list, key=lambda x: (x['year'], x['week']))
    return sorted_data

def OptimalOrderCalculationOneWeek():
    # Fetch all necessary data before the loop
    materials = Material.query.all()
    options = Options.query.first()
    suppliers = Supplier.query.filter(Supplier.availability == True).all()
    prices = Price.query.filter(Price.end_date.is_(None)).join(Supplier).filter(Supplier.id == Price.supplier_id).filter(Supplier.availability == True).all()
    materials_per_supplier = MaterialsPerSupplier.query.join(Supplier).filter(Supplier.id == MaterialsPerSupplier.supplier_id).filter(Supplier.availability == True).all()
    weekly_material_demands = WeeklyMaterialDemand.query.all()
    outstanding_orders = Order.query.filter(Order.delivery_date.is_(None)).join(Supplier).filter(Supplier.id == Order.supplier_id).filter(Supplier.availability == True).all()
    weeks = Week.query.all()

    # Preprocess data for quick lookup
    supplier_dict = {supplier.id: supplier for supplier in suppliers}
    price_dict = {(price.supplier_id, price.material_id): price for price in prices}
    materials_per_supplier_dict = {(mps.supplier_id, mps.material_id): mps for mps in materials_per_supplier}
    weekly_material_demands_dict = {}
    for demand in weekly_material_demands:
        if demand.material_id not in weekly_material_demands_dict:
            weekly_material_demands_dict[demand.material_id] = []
        weekly_material_demands_dict[demand.material_id].append(demand)
    outstanding_orders_dict = {}
    for order in outstanding_orders:
        if order.material_id not in outstanding_orders_dict:
            outstanding_orders_dict[order.material_id] = []
        outstanding_orders_dict[order.material_id].append(order)
    
    week_dict = {f"wk{week.week}_{week.year}": week for week in weeks}
    
    rec_order_dict = {}

    today = date.today()
    
    for material in materials:
        material_id = material.id
        unit = material.unit.name if material.unit else None
        name = material.name
        strategy = material.strategy.value if material.strategy else options.strategy.value
        supplier = None
        
        if strategy == "Sustainability":
            valid_suppliers = [s for s in suppliers if (s.id, material_id) in materials_per_supplier_dict and s.sustainability_index is not None]
            if valid_suppliers:
                supplier = max(valid_suppliers, key=lambda s: s.sustainability_index)
            else:   
                continue
        elif strategy == "Risk":
            valid_suppliers = [s for s in suppliers if (s.id, material_id) in materials_per_supplier_dict and s.risk_index is not None]
            if valid_suppliers:
                supplier = max(valid_suppliers, key=lambda s: s.risk_index)
            else:
                continue
        elif strategy == "Price":
            valid_prices = [p for p in prices if p.material_id == material_id and p.cost is not None]
            if valid_prices:
                cheapest_price = min(valid_prices, key=lambda p: p.cost)
                supplier = supplier_dict[cheapest_price.supplier_id]
            else:
                continue
        elif strategy == "LeadTime":
            valid_materials = [mps for mps in materials_per_supplier if mps.material_id == material_id and mps.lead_time is not None]
            if valid_materials:
                shortest_lead_time = min(valid_materials, key=lambda mps: mps.lead_time)
                supplier = supplier_dict[shortest_lead_time.supplier_id]
            else:
                continue
        
        if not supplier:
            continue
        
        lt = materials_per_supplier_dict[(supplier.id, material_id)]
        
        if not lt.lead_time:
            continue
        
        supplier_id = supplier.id
        price = price_dict.get((supplier_id, material_id))
        price = price.cost if price else None
        
        if not price:
            continue
        
        mps = materials_per_supplier_dict.get((supplier_id, material_id))
        lead_time = mps.lead_time
        co2_emissions = mps.co2_emissions
        
        sustainability_index = supplier.sustainability_index
        risk_index = supplier.risk_index
        
        weekly_material_demand = weekly_material_demands_dict.get(material_id, [])
        filtered_weekly_material_demand = [record for record in weekly_material_demand if record.is_later_or_equal]
        
        week = 0
        
        week_start = today + timedelta(weeks=week)
        week_number = week_start.isocalendar()[1]
        year = week_start.isocalendar()[0]
        week_key = f"wk{week_number}_{year}"

        lead_time_demand = get_lead_time_demand(filtered_weekly_material_demand, lead_time, week_start)
                    
        # Calculate total outstanding orders for the material within the lead time
        total_outstanding_orders = 0
        if material_id in outstanding_orders_dict:
            for order in outstanding_orders_dict[material_id]:
                if is_within_lead_time(order.planned_delivery_date, lead_time, week_start):
                    total_outstanding_orders += order.amount
        total_demand = lead_time_demand + material.safety_stock - total_outstanding_orders
        
        if total_demand <= material.stock_level:
            continue
        else:
            min_order = total_demand - material.stock_level
            material_recommendation = {
                "material_id": material_id,
                "unit": unit,
                "name": name,
                "strategy": strategy,
                "min_order": min_order,
                "supplier_id": supplier_id,
                "supplier_name": supplier.name,
                "lead_time": lead_time,
                "sustainability_index": sustainability_index,
                "risk_index": risk_index,
                "price": price,
            }
            if week_key not in rec_order_dict:
                rec_order_dict[week_key] = []
                
            if is_new_material(rec_order_dict,material_id):
                rec_order_dict[week_key].append(material_recommendation)
    return rec_order_dict[week_key]
    
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
    
    # Fetch all needed week IDs in one query
    weeks_to_query = {(year, week) for _, year, week in material_demand_dict.keys()}
    week_dict = {
        (wk.year, wk.week): wk.id
        for wk in Week.query.filter(
            db.or_(
                db.and_(Week.year == year, Week.week == week)
                for year, week in weeks_to_query
            )
        ).all()
    }
    
    # Add new data
    for (material_id, year, week), amount in material_demand_dict.items():
        week_id = week_dict.get((year, week))
        if week_id is not None:
            weekly_demand = WeeklyMaterialDemand(
                material_id=material_id,
                week_id=week_id,
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

# Helper function to calculate lead time demand
def get_lead_time_demand(weekly_material_demand, lead_time, week_start):
    total_demand = 0
    lead_time_end_date = week_start + timedelta(weeks=lead_time)
    for demand in weekly_material_demand:
        if demand.is_in_lead_time(lead_time_end_date):
            total_demand += demand.amount
    return total_demand

# Helper function to determine if a date is within lead time
def is_within_lead_time(planned_delivery_date, lead_time, week_start):
    lead_time_end_date = week_start + timedelta(weeks=lead_time+2)
    return planned_delivery_date <= lead_time_end_date

def is_new_material(data, material_id):
    for week in data.values():
        for material in week:
            if material['material_id'] == material_id:
                return False
    return True

def MaterialDemand5Weeks():
    # Fetch Base Production Data for each product with all weeks later than Current week, weekly basis
    external_production_data = ExternalProductionData.query.all()
    
    filtered_external_production_data = [record for record in external_production_data if record.is_later_or_equal]
    
    # Fetch the Project Data, weekly basis (next month)
    product_per_projects_all = Project.query.join(ProductsPerProject).filter(Project.id==ProductsPerProject.project_id).add_columns(Project.id,Project.start_week,Project.end_week,ProductsPerProject.amount, ProductsPerProject.product_id).all()
    
    filtered_product_per_projects = [project for project in product_per_projects_all if project.Project.check_project_week()]
    
    # Fetch Data for Product composition
    materials_per_products = MaterialsPerProduct.query.all()
    
    # Calculate weekly total Product demand (Sum of Demands)
    weekly_total = get_weekly_totals(filtered_external_production_data, filtered_product_per_projects)
    
    # Calculate weekly total Material demand (Demand and Composition fit)
    material_demand_dict = calculate_material_demand(weekly_total,materials_per_products)
    
    result = aggregate_demand(material_demand_dict,False)
    
    return result

def ProductDemand5Weeks():
    # Fetch Base Production Data for each product with all weeks later than Current week, weekly basis
    external_production_data = ExternalProductionData.query.all()
    
    filtered_external_production_data = [record for record in external_production_data if record.is_later_or_equal]
    
    # Fetch the Project Data, weekly basis (next month)
    product_per_projects_all = Project.query.join(ProductsPerProject).filter(Project.id==ProductsPerProject.project_id).add_columns(Project.id,Project.start_week,Project.end_week,ProductsPerProject.amount, ProductsPerProject.product_id).all()
    
    filtered_product_per_projects = [project for project in product_per_projects_all if project.Project.check_project_week()]
    
    # Calculate weekly total Product demand (Sum of Demands)
    weekly_total = get_weekly_totals(filtered_external_production_data, filtered_product_per_projects)
    
    result = aggregate_demand(weekly_total,True)        

    return result

def get_next_weeks(year, week, num_weeks=5):
    current_date = datetime.strptime(f'{year}-W{week-1}-1', "%Y-W%U-%w")
    next_weeks = []
    for _ in range(num_weeks):
        current_date += timedelta(weeks=1)
        next_weeks.append((current_date.isocalendar()[0], current_date.isocalendar()[1]))
    return next_weeks

def aggregate_demand(data,product=False):
    demand_aggregate = defaultdict(float)

    # Fetch material and product details from the database
    materials = {material.id: {'name': material.name, 'stock_level': material.stock_level, 'unit': material.unit.name if material.unit else ""} for material in Material.query.all()}
    products = {product.id: {'description': product.description, 'specification': product.specification} for product in Product.query.all()}
      
    
    for (id, year, week), demand in data.items():
        next_weeks = get_next_weeks(year, week, num_weeks=5)
        for next_year, next_week in next_weeks:
            if (id, next_year, next_week) in data:
                demand_aggregate[id] += data[(id, next_year, next_week)]
    
    if product:
        total_demand_sum = sum(demand_aggregate.values())
        return [
            {
                "product_id": id, 
                "demand_sum": round(demand_sum,2),
                "description": products[id]['description'] if id in products else None,
                "specification": products[id]['specification'] if id in products else None,
                "percentage_of_total_output": round(demand_sum / total_demand_sum * 100) if total_demand_sum > 0 else 0
            }
            for id, demand_sum in demand_aggregate.items()
        ]
    else:
        return [
            {
                "material_id": id, 
                "demand_sum": round(demand_sum,2),
                "unit": materials[id]['unit'],
                "material_name": materials[id]['name'] if id in materials else None,
                "percentage_of_current_stock": round(demand_sum / materials[id]['stock_level'] * 100) if id in materials and materials[id]['stock_level'] > 0 else 0
            }
            for id, demand_sum in demand_aggregate.items()
        ]
