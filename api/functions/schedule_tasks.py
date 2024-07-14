# import external packages
from datetime import datetime
# import functions and data
from functions.fetch_updates import update_or_create_materials, update_or_create_orders
from functions.risk_calculation import update_supplier_risk_indices
from functions.sustainability_calculations import calculate_sustainability_index
from functions.reliability_calculation import ReliabilityCalculation

# Function to schedule daily tasks
def Run():
    update_or_create_orders()
    update_or_create_materials()
    update_supplier_risk_indices()
    calculate_sustainability_index()
    ReliabilityCalculation()
    print(f'Task executed at {datetime.now()}')