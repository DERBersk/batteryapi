# Show Multiple Prices

Show data of a All Prices.

**URL** : `/api/price/`

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
        "cost": 3.3593354279833076,
        "end_date": "Sun, 21 Jul 2024 00:00:00 GMT",
        "id": 1,
        "material_id": 4,
        "start_date": "Thu, 30 May 2024 00:00:00 GMT",
        "supplier_id": 3,
        "unit": "meter"
    },
    {
        "cost": 16.348074224725764,
        "end_date": "Fri, 14 Feb 2025 00:00:00 GMT",
        "id": 2,
        "material_id": 4,
        "start_date": "Mon, 20 May 2024 00:00:00 GMT",
        "supplier_id": 1,
        "unit": "meter"
    },
    ...
]
```

# Show Single Price

Show data of a single Price.

**URL** : `/api/price/<material_id>`

**URL Parameters** : `material_id=[integer]` where `material_id` is the id of the Material associated with the Price.

**Method** : `GET`

**Data**: 

```json
{
    
}
```

## Success Response

**Condition** : If Price with material_id and an empty end-date (meaning it is still in place) exists.

**Code** : `200 OK`

**Content example**:

```json
{
    "id": 1,
    "cost": 3.35,
    "end_date": "Sun, 21 Jul 2024 00:00:00 GMT",
    "material_id": 4,
    "start_date": "Thu, 30 May 2024 00:00:00 GMT",
    "supplier_id": 3,
    "unit": "meter"
}
```

## Error Responses

**Condition** : If Price does not exist with `material_id` of provided `material_id` parameter and an empty end_date.

**Code** : `404 NOT FOUND`

**Content** : `{'message': 'Price with material_id {material_id} and empty end_date not found'}`