# import external packages
import numpy as np
# import functions and data
from extensions import db
# import models
from models.materials_per_supplier import MaterialsPerSupplier
from models.supplier import Supplier

# Normalization function
def normalize(value, max_value):
    if max_value == 0:
        return 0.5
    else:
        return (value) / (max_value)

# Calculate Euclidean norm (Green Value)
def euclidean_norm(values):
    return np.sqrt(sum(val ** 2 for val in values))


def calculate_sustainability_index():
    # Fetch all MaterialsPerSupplier records
    materials_per_supplier = MaterialsPerSupplier.query.order_by(MaterialsPerSupplier.supplier_id.asc()).all()
    
    # Group data by material and supplier
    material_supplier_data = {}
    for mps in materials_per_supplier:
        if mps.material_id not in material_supplier_data:
            material_supplier_data[mps.material_id] = {}
        if mps.supplier_id not in material_supplier_data[mps.material_id]:
            material_supplier_data[mps.material_id][mps.supplier_id] = {
                'co2_emissions': [],
                'distances': []
            }
        if mps.co2_emissions is not None:
            material_supplier_data[mps.material_id][mps.supplier_id]['co2_emissions'].append(mps.co2_emissions)
        if mps.distance is not None:
            material_supplier_data[mps.material_id][mps.supplier_id]['distances'].append(mps.distance)    
    # Calculate normalized values and green value for each supplier
    green_values = {}
    for material_id, suppliers in material_supplier_data.items():
        # Collect all co2 and distance values for normalization
        all_co2_values = []
        all_distance_values = []
        for data in suppliers.values():
            all_co2_values.extend(data['co2_emissions'])
            all_distance_values.extend(data['distances'])
        
        co2_max = max(all_co2_values) if all_co2_values else 1
        distance_max = max(all_distance_values) if all_distance_values else 1
        
        for supplier_id, data in suppliers.items():
            co2_values = data['co2_emissions']
            distance_values = data['distances']
            
            if not co2_values or not distance_values:
                continue
            
            # Normalize values
            normalized_co2_values = [normalize(value, co2_max) for value in co2_values]
            normalized_distance_values = [normalize(value, distance_max) for value in distance_values]
            
            # Calculate average normalized values
            avg_normalized_co2 = np.mean(normalized_co2_values)
            avg_normalized_distance = np.mean(normalized_distance_values)
            
            # Calculate green value (Euclidean norm)
            green_value = euclidean_norm([avg_normalized_co2, avg_normalized_distance])
            
            # Accumulate the green value for each supplier
            if supplier_id not in green_values:
                green_values[supplier_id] = []
            green_values[supplier_id].append(green_value)
    
    # Calculate average green value for each supplier
    supplier_sustainability_index = {supplier_id: np.mean(values) for supplier_id, values in green_values.items()}
    
    # Update sustainability_index in the Supplier table
    for supplier_id, green_value in supplier_sustainability_index.items():
        supplier = Supplier.query.filter(Supplier.id == supplier_id).first()
        if supplier:
            supplier.sustainability_index = float(round(green_value / np.sqrt(2),3))
    
    # Commit the changes to the database
    db.session.commit()
    
    suppliers = Supplier.query.all()
    return [supplier.serialize() for supplier in suppliers]