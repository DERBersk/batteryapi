# Show MaterialsPerSupplier Without allocated active Price

Show Material Per Supplier entries Without allocated active Price

**URL** : `/api/kpi/MaterialPerSupplierWithoutPrice`

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
    "count": 2,
    "data": [
        {
        "co2_emissions": 111.0,
        "distance": 20.0,
        "id": 11,
        "lead_time": 4,
        "material_id": 64,
        "supplier_id": 19
        },
        {
        "co2_emissions": 1234.0,
        "distance": 10.0,
        "id": 12,
        "lead_time": 2,
        "material_id": 65,
        "supplier_id": 19
        }
    ]
}
```