# import external packages
from datetime import datetime

from functions.fetch_updates import update_or_create_materials, update_or_create_orders

# Function to schedule daily tasks
def Run():
    update_or_create_orders()
    update_or_create_materials()
    print(f'Task executed at {datetime.now()}')