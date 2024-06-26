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
        "country": "Germany",
        "email": "",
        "external_id":"ROTTERDAM-12",
        "materials": [
            {
                "id": 2,
                "lead_time": 3,
                "co2_emissions": 2200,
                "distance": 20                 
            },
            {
                "name": "New Zinc",
                "lead_time": 2,
                "co2_emissions": 10,
                "distance": 1500  
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
        "country": "USA",
        "email": "maxmustermann@gmail.com",
        "external_id":"afwf-1411",
        "materials": [
            {
                "id": 1,
                "lead_time": 1,
                "co2_emissions": 100,
                "distance": 5  
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

### 400 Bad Request

**Condition** : If the format is not given as a List

**Code** : `400 Bad request`

**Content** : 

`{'message': 'Invalid data format. Expected a list of Suppliers.'}`

