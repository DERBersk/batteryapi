# Show Multiple Material

Show data of a All Materials.

**URL** : `/api/materials/`

**Method** : `GET`

**Data**: 

```json
{
    
}
```

## Success Response

**Code** : `200 OK`

**Content example**:

```json
[
    {
        "id": 1,
        "lot_size": 9,
        "name": "Lithium-Ion",
        "safety_stock": 7,
        "stock_level": 86,
        "strategy": "Sustainability"
    },
    {
        "id": 2,
        "lot_size": 5,
        "name": "Copper",
        "safety_stock": 8,
        "stock_level": 32.7,
        "strategy": "Price"
    },
    ...
]
```

# Show Single Material

Show data of a single Material.

**URL** : `/api/materials/<material_id>`

**URL Parameters** : `material_id=[integer]` where `material_id` is the ID of the Material.

**Method** : `GET`

**Data**: 

```json
{
    
}
```

## Success Response

**Condition** : If Material exists.

**Code** : `200 OK`

**Content example**:

```json
{
    "id": 1,
    "lot_size": 9,
    "name": "Copper",
    "safety_stock": 7,
    "stock_level": 86.95,
    "strategy": " "
}
```

## Error Responses

**Condition** : If Material does not exist with `id` of provided `material_id` parameter.

**Code** : `404 NOT FOUND`

**Content** : `{'message': 'Material with id {material_id} not found'}`