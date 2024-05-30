# File for Order Calculation Function
def MaterialDemandCalculation():
    # Fetch or Create Forecasting Data for each product with all weeks later than Current week, weekly basis
    
    # Fetch the Project Data, weekly basis (next month)
    
    # Fetch Data for Product composition
    
    # Calculate weekly total Product demand (Sum of Demands)
    
    # Calculate weekly total Material demand (Demand and Composition fit)
    
    # Save Data in new Table Material Demand (if Data already exists, update data)

    return ""

def OptimalOrderCalculation():
    # Fetch weekly Material Demand Data
    
    # Fetch Lead times
    
    # Fetch Safety Stock
    
    # If Inventory smaller than Safety Stock: Order needed anyway
    
    # Fetch Supplier for Material each after employed strategy
    
    # For each of the Materials
    
        # Aggregate Demanded Material in lead time (of Supplier) area (5 days lead time = Material Demand next 2 weeks (weeks rounded up +1))
    
        # If Demanded Material is smaller than the inventory: Recommend no order
        
        # If Demanded Material is bigger than the inventory: Recommend order
        
    # Return List of recommended orders
    
    return ""