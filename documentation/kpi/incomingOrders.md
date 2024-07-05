# Show all incoming Orders

Show a list of all incoming orders (meaning delivery date is empty)

**URL** : `/api/kpi/incomingOrders`

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
    "material_id": 11,
    "supplier_id": 12,
    "amount": 150,
    "planned_delivery_date": "20.06.2024",
    "delivery_date": None,
    "unit": "kg"
  }
  ...
]
```