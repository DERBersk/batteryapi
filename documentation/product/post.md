# Create Products and Connected Tables

Create or modify one or many Products and each respective fitted table (MaterialsPerProduct, Material)

**URL** : `/api/products/`

**Method** : `POST`

**Comment** : For the Product and for the Materials: If the id is not given, a new instance is created. If the id is given, the instance is expected to exist and created in a new fashion. The MaterialsPerProduct is deleted for the Product so that every given instance is then every existing instance for the respective Product

**Data example** All fields must be sent except id.

```json
[
    {
        "id": 1,
        "description": "Changed Product A",
        "specification": "Specification for Product A",
        "materials": [
        {
            "name": "New Material X",
            "safety_stock": 100,
            "lot_size": 50,
            "stock_level": 200,
            "amount": 50
        },
        {
            "id": 1,
            "name": "Changed Material Y",
            "safety_stock": 150,
            "lot_size": 75,
            "stock_level": 300,
            "amount": 100
        }
        ]
    },
    {
        "description": "New Product B",
        "specification": "Specification for Product B",
        "materials": [
        {
            "name": "New Material Z",
            "safety_stock": 120,
            "lot_size": 60,
            "stock_level": 250,
            "amount": 75
        }
        ]
    }
]
```

## Success Response

**Condition** : If everything is OK and for all given id, a respective instance exists.

**Code** : `201 CREATED`

**Content example**: `{'message': 'Products created/updated successfully'}`

## Error Responses

### 404 Not Found

**Condition** : Either a product id is given without it existing in the database or a material id is given without it existing.

**Code** : `404 NOT FOUND`

**Content** : 

`{'message': 'Material with id {material_id} not found'}`

`{'message': 'Product with id {product_id} not found'}`

### 400 Bad Request

**Condition** : If the format is not given as a List

**Code** : `400 Bad request`

**Content** : 

`{'message': 'Invalid data format. Expected a list of prices.'}`