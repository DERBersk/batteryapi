# Create Orders

Create or modify one or many Orders

**URL** : `/api/order/`

**Method** : `POST`

**Data example** All fields must be sent except id, if id is given, the data is modified.

```json
[
    {
        "material_id": 101,
        "supplier_id": 201,
        "amount": 50.5,
        "planned_delivery_date": "2024-06-10",
        "delivery_date": "2024-06-09"
    },
    {
        "id": 2,
        "material_id": 102,
        "supplier_id": 202,
        "amount": 75.0,
        "planned_delivery_date": "2024-06-12",
        "delivery_date": "2024-06-13"
    },
    {
        "material_id": 103,
        "supplier_id": 203,
        "amount": 100.0,
        "planned_delivery_date": "2024-06-15",
        "delivery_date": null
    }
]
```

## Success Response

**Condition** : If everything is OK and for all given id, a respective instance exists.

**Code** : `201 CREATED`

**Content example**: `{'message': 'Orders added/updated successfully'}`

## Error Responses

### 404 Not Found

**Condition** : An order id is given without it existing in the database

**Code** : `404 NOT FOUND`

**Content** : 

`{'message': 'Order with id {order_id} not found'}`

### 400 Bad Request

**Condition** : If the format is not given as a List

**Code** : `400 Bad request`

**Content** : 

`{'message': 'Invalid data format. Expected a list of Orders.'}`

