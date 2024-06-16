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
[
    {
        "id": 20,
        "lot_size": 3.0,
        "name": "Leitadditiv 2",
        "safety_stock": 100.0,
        "stock_level": 99.0,
        "strategy": null,
        "unit": null
    },
    {
        "id": 82,
        "lot_size": 1.0,
        "name": "SuperC45",
        "safety_stock": 100.0,
        "stock_level": 99.0,
        "strategy": null,
        "unit": null
    },
    ...
]
```