# Show Multiple Orders

Show data of a All Orders.

**URL** : `/api/order/`

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
        "id": 3,
        "material_id": 103,
        "supplier_id": 203,
        "amount": 100.0,
        "planned_delivery_date": "2024-06-15",
        "delivery_date": null
    }
]
```

