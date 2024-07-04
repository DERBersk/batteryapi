# Show all Materials without an assigned Supplier

Show critical Materials, meaning Materials that do not have an existing connection to a Supplier.

**URL** : `/api/kpi/materialWithoutSupplier`

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
{
    "count": 79,
    "data": [
        {
        "external_id": "M1589",
        "id": 16,
        "lot_size": 136.0,
        "name": "L\u00f6semittel (Wasser) - 50%",
        "safety_stock": 100.0,
        "stock_level": 99.0,
        "strategy": null,
        "unit": "ml"
        },
        {
        "external_id": "M7090",
        "id": 17,
        "lot_size": 136.0,
        "name": "Kathodenmaterial (Solid Content 70%)",
        "safety_stock": 100.0,
        "stock_level": 99.0,
        "strategy": null,
        "unit": "ml"
        },
        ...
    ]
}   
```