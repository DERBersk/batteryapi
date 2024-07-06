# Show material Demands accumulated over the next 5 weeks

**URL** : `/api/kpi/materialDemand5Weeks`

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
        "demand_sum": 74250.0,
        "material_id": 11,
        "material_name": "Anodenmaterial (Solid content 50%)"
    },
    {
        "demand_sum": 243750.0,
        "material_id": 12,
        "material_name": "Graphit"
    },
    {
        "demand_sum": 3060.0,
        "material_id": 13,
        "material_name": "Leitadditiv"
    },
    {
        "demand_sum": 9000.0,
        "material_id": 14,
        "material_name": "Binder 1 (SBR)"
    },
    {
        "demand_sum": 12000.0,
        "material_id": 15,
        "material_name": "Binder 2 (CMC)"
    }
]
```