import random
from datetime import datetime, timedelta, time
from faker import Faker
from extensions import db
from models.supplier import Supplier
from models.material import Material
from models.product import Product
from models.project import Project
from models.price import Price
from models.demand import Demand
from models.time import Time
from models.materials_per_product import MaterialsPerProduct
from models.materials_per_supplier import MaterialsPerSupplier
from models.products_per_project import ProductsPerProject

def populate_suppliers(num_suppliers=5):
    fake = Faker()
    for _ in range(num_suppliers):
        name = fake.company()
        lat = random.uniform(-90, 90)
        long = random.uniform(-180, 180)
        risk_index = random.uniform(0, 10)
        sustainability_index = random.uniform(0, 10)
        quality = random.uniform(0, 10)
        supplier = Supplier(name=name, lat=lat, long=long, risk_index=risk_index, sustainability_index=sustainability_index, quality=quality)
        db.session.add(supplier)
    db.session.commit()
        
def populate_materials(num_materials=5):
    fake = Faker()
    for _ in range(num_materials):
        name = fake.word()
        safety_stock = random.randint(1, 10)
        lot_size = random.randint(1, 10)
        stock_level = random.uniform(0, lot_size*10)
        material = Material(name=name, safety_stock=safety_stock, lot_size=lot_size, stock_level=stock_level)
        db.session.add(material)
    db.session.commit()
        
def populate_products(num_products=5):
    fake = Faker()
    for _ in range(num_products):
        name = fake.word()
        product = Product(name=name)
        db.session.add(product)
    db.session.commit()
    
def populate_projects(num_projects=5):
    fake = Faker()
    for _ in range(num_projects):
        partner = fake.company()
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(1, 365))
        production_schedule = random.choice(['static'])
        project = Project(partner=partner, start_date=start_date, end_date=end_date, production_schedule=production_schedule)
        db.session.add(project)
    db.session.commit()
        
def populate_demands(num_demands=20):
    # Assuming you have a Product and Time model defined
    # Replace 'Product' and 'Time' with your actual models
    product_ids = [1, 2, 3, 4, 5]  # Sample product IDs
    time_slots = [1, 2, 3, 4]  # Sample time slots

    for _ in range(num_demands):
        product_id = random.choice(product_ids)
        time_slot = random.choice(time_slots)
        order_count = random.randint(1, 100)
        amount = random.randint(100, 1000)
        demand = Demand(product_id=product_id, time_slot=time_slot, order_count=order_count, amount=amount)
        db.session.add(demand)
    db.session.commit()
    
def populate_times(num_times=4):
    for _ in range(num_times):
        name = f"Time {_}"
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(1, 30))
        time = Time(name=name, start_date=start_date, end_date=end_date)
        db.session.add(time)
    db.session.commit()

def populate_prices(num_prices=20):
    material_ids = [1, 2, 3, 4, 5]  # Sample material IDs
    supplier_ids = [1, 2, 3, 4, 5]  # Sample supplier IDs
    units = ['kg', 'meter', 'unit']  # Sample units

    for _ in range(num_prices):
        material_id = random.choice(material_ids)
        supplier_id = random.choice(supplier_ids)
        cost = random.uniform(1, 100)
        unit = random.choice(units)
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(1, 365))
        price = Price(material_id=material_id, supplier_id=supplier_id, cost=cost, unit=unit, start_date=start_date, end_date=end_date)
        db.session.add(price)
    db.session.commit()
    
def populate_materials_per_supplier(num_entries=20):
    material_ids = [1, 2, 3, 4, 5]  # Sample material IDs
    supplier_ids = [1, 2, 3, 4, 5]  # Sample supplier IDs

    for _ in range(num_entries):
        material_id = random.choice(material_ids)
        supplier_id = random.choice(supplier_ids)
        min_amount = random.randint(1, 100)
        # Generate a random delivery time between 1 hour and 24 hours
        lead_time = time(hour=random.randint(0, 23))
        availability = random.uniform(0, 1)
        entry = MaterialsPerSupplier(material_id=material_id, supplier_id=supplier_id, min_amount=min_amount, lead_time=lead_time, availability=availability)
        db.session.add(entry)
    db.session.commit()

def populate_materials_per_product(num_entries=20):
    material_ids = [1, 2, 3, 4, 5]  # Sample material IDs
    product_ids = [1, 2, 3, 4, 5]  # Sample product IDs

    for _ in range(num_entries):
        material_id = random.choice(material_ids)
        product_id = random.choice(product_ids)
        amount = random.randint(1, 100)
        entry = MaterialsPerProduct(material_id=material_id, product_id=product_id, amount=amount)
        db.session.add(entry)
    db.session.commit()

def populate_products_per_project(num_entries=20):
    product_ids = [1, 2, 3, 4, 5]  # Sample product IDs
    project_ids = [1, 2, 3, 4, 5]  # Sample project IDs

    for _ in range(num_entries):
        product_id = random.choice(product_ids)
        project_id = random.choice(project_ids)
        amount = random.randint(1, 100)
        entry = ProductsPerProject(product_id=product_id, project_id=project_id, amount=amount)
        db.session.add(entry)
    db.session.commit()
