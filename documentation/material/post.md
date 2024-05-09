# Create Material and Connected Tables

Create or modify one or many Materials.

**URL** : `/api/materials/`

**Method** : `POST`

**Data example** All fields must be sent except id.

```json
[
  {
    "id": 1,
    "name": "Changed Material X",
    "safety_stock": 100,
    "lot_size": 50,
    "stock_level": 200
  },
  {
    "name": "New Material Y",
    "safety_stock": 150,
    "lot_size": 75,
    "stock_level": 300
  }
]
```

## Success Response

**Condition** : If everything is OK and for all given id, a respective instance exists.

**Code** : `201 CREATED`

**Content example**: `{'message': 'Materials created/updated successfully'}`

## Error Responses

### 404 Not Found

**Condition** : A Material id is given without it existing in the database.

**Code** : `404 NOT FOUND`

**Content** : 

`{'message': 'Material with id {Material_id} not found'}`

### 400 Bad Request

**Condition** : If the format is not given as a List

**Code** : `400 Bad request`

**Content** : 

`{'message': 'Invalid data format. Expected a list of prices.'}`

