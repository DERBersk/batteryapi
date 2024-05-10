# Create Suppliers and Connected Tables

Create or modify one or many Suppliers and each respective fitted table (MaterialsPerSupplier, Material)

**URL** : `/api/supplier/`

**Method** : `POST`

**Comment** : For the Supplier and for the Materials: If the id is not given, a new instance is created. If the id is given, the instance is expected to exist and created in a new fashion. The MaterialsPerSupplier is deleted for the supplier so that every given instance is then every existing instance for the respective supplier

**Data example** All fields must be sent except id.

```json
[
    {
        "name": "New Supplier",
        "lat": 40.7128,
        "long": -74.0060,
        "risk_index": 3,
        "sustainability_index": 7,
        "quality": 8,
        "reliability": 9,
        "availability": "True",
        "materials": [
        {
            "id": 2,
            "name": "Changed Copper",
            "safety_stock": 100,
            "lot_size": 50,
            "stock_level": 200,
            "min_amount": 20,
            "max_amount": 100,
            "lead_time": "05:00:00",
            "availability": 95,
            "volume_commitment": 200
        },
        {
            "name": "New Zinc",
            "safety_stock": 150,
            "lot_size": 75,
            "stock_level": 300,
            "min_amount": 30,
            "max_amount": 150,
            "lead_time": "07:00:00",
            "availability": 90,
            "volume_commitment": 300
        }
        ]
    },
    {
        "id": 3,
        "name": "Changed Supplier",
        "lat": 34.0522,
        "long": -118.2437,
        "risk_index": 4,
        "sustainability_index": 6,
        "quality": 7,
        "reliability": 8,
        "availability": "False",
        "materials": [
        {
            "id": 1,
            "name": "Changed Lithium-Ion",
            "safety_stock": 120,
            "lot_size": 60,
            "stock_level": 250,
            "min_amount": 25,
            "max_amount": 120,
            "lead_time": "06:00:00",
            "availability": 85,
            "volume_commitment": 250
        }
        ]
    }
]
```

## Success Response

**Condition** : If everything is OK and for all given id, a respective instance exists.

**Code** : `201 CREATED`

**Content example**: `{'message': 'Suppliers created/updated successfully'}`

## Error Responses

### 404 Not Found

**Condition** : Either a supplier id is given without it existing in the database or a material id is given without it existing.

**Code** : `404 NOT FOUND`

**Content** : 

`{'message': 'Material with id {material_id} not found'}`

`{'message': 'Supplier with id {supplier_id} not found'}`

