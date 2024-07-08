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
        "distance": 21.0,
        "id": 11,
        "lead_time": 4,
        "material_id": 64,
        "material_name": "Texturecel 30000 P BA",
        "supplier_id": 19,
        "supplier_name": "Dupont (Test)"
        },
        {
        "co2_emissions": 1234.0,
        "distance": 10.0,
        "id": 12,
        "lead_time": 2,
        "material_id": 65,
        "material_name": "C-Nergy Super C 45 ",
        "supplier_id": 19,
        "supplier_name": "Dupont (Test)"
        }
    ]
}
```