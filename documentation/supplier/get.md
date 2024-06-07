# Show Multiple Suppliers

Show data of a All Suppliers.

**URL** : `/api/supplier/`

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
        "availability": 0.4520782188395973,
        "id": 1,
        "lat": -68.37832013303877,
        "long": -72.47398735322135,
        "name": "Fisher-Diaz",
        "quality": 5.924827825576889,
        "reliability": 0.3174353388376102,
        "risk_index": 0.8108719323659386,
        "sustainability_index": 8.28791629020131,
        "availability": "True",
        "country": "France",
        "email": ""
    },
    {
        "availability": 0.9874379222633706,
        "id": 2,
        "lat": -37.9774473130205,
        "long": -139.9946895181667,
        "name": "Martinez LLC",
        "quality": 4.117976905451678,
        "reliability": 0.3862772420817989,
        "risk_index": 2.6539343594064366,
        "sustainability_index": 6.025667519196149,
        "availability": "False",
        "country": "China",
        "email": "maxmustermann@gmail.com"
    },
    ...
]
```

# Show Single Supplier

Show data of a single Supplier and its associated tables: Material, Price and MaterialsPerSupplier 

**URL** : `/api/supplier/<supplier_id>`

**URL Parameters** : `supplier_id=[integer]` where `supplier_id` is the ID of the Supplier.

**Method** : `GET`

**Data**: 

```json
{
    
}
```

## Success Response

**Condition** : If Supplier exists.

**Code** : `200 OK`

**Content example**:

```json
{
    "id": 1,
    "availability": 0.45,
    "lat": -68.37832013303877,
    "long": -72.47398735322135,
    "country": "Chile",
    "materials": [
        {
            "id": 1,
            "lead_time": "14:00:00",
            "lot_size": 9,
            "name": "Cobalt",
            "price": 10.95,
            "safety_stock": 7,
            "stock_level": 86,
        }
    ],
    "name": "Fisher-Diaz",
    "quality": 5.92,
    "reliability": 0.317,
    "risk_index": 0.81,
    "sustainability_index": 8.28,
    "email": "monikamustermann@fisher.ch"
}
```

## Error Responses

**Condition** : If Supplier does not exist with `id` of provided `supplier_id` parameter.

**Code** : `404 NOT FOUND`

**Content** : `{'message': 'Supplier with id {supplier_id} not found'}`