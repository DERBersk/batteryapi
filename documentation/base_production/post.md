# Create Base Production Volumes

Create or modify one or many Base Production Volumes

**URL** : `/api/baseproduction/`

**Method** : `POST`

**Data example** All fields must be sent except id, if id is given, the data is modified.

```json
[
    {
        "product_id": 1,
        "week_id": "wk02_2025",
        "amount": 100
    },
    {
        "id": 1,
        "product_id": 2,
        "week_id": "wk03_2025",
        "amount": 150
    }
]
```

## Success Response

**Condition** : If everything is OK and for all given id, a respective instance exists.

**Code** : `201 CREATED`

**Content example**: `{'message': 'Base production volumes added/updated successfully'}`

## Error Responses

### 404 Not Found

**Condition** : A base production volume id is given without it existing in the database

**Code** : `404 NOT FOUND`

**Content** : 

`{'message': 'Base Production Volume with id {base_production_id} not found'}`

### 400 Bad Request

**Condition** : If the format is not given as a List

**Code** : `400 Bad request`

**Content** : 

`{'message': 'Invalid data format. Expected a list of Base Production Volumes.'}`

