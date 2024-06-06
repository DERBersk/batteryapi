# Create Price and Connected Tables

Create or modify one or many Prices.

**URL** : `/api/price/`

**Method** : `POST`

**Data example** All fields must be sent except id.

```json
[
    {
        "id": 1,
        "material_id": 123,
        "supplier_id": 456,
        "cost": 10.99,
        "unit": "USD",
        "start_date": "2024-05-10",
        "end_date": "2024-06-10"
    },
    {
        "material_id": 456,
        "supplier_id": 789,
        "cost": 20.55,
        "unit": "USD",
        "start_date": "2024-06-01",
        "end_date": "2024-07-01"
    }
]
```

## Success Response

**Condition** : If everything is OK and for all given id, a respective instance exists.

**Code** : `201 CREATED`

**Content example**: `{'message': 'Prices created/updated successfully'}`

## Error Responses

### 404 Not Found

**Condition** : A Price id is given without it existing in the database.

**Code** : `404 NOT FOUND`

**Content** : 

`{'message': 'Price with id {price_id} not found'}`

### 400 Bad Request

**Condition** : If the format is not given as a List

**Code** : `400 Bad request`

**Content** : 

`{'message': 'Invalid data format. Expected a list of prices.'}`

