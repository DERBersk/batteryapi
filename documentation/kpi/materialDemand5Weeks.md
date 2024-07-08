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
    "demand_sum": 270180.0,
    "material_id": 11,
    "material_name": "Anodenmaterial (Solid content 50%)",
    "percentage_of_current_stock": 272909,
    "unit": "g"
  },
  {
    "demand_sum": 819350.0,
    "material_id": 12,
    "material_name": "Graphit",
    "percentage_of_current_stock": 827626,
    "unit": "kg"
  },
  {
    "demand_sum": 10526.25,
    "material_id": 13,
    "material_name": "Leitadditiv",
    "percentage_of_current_stock": 10633,
    "unit": "g"
  },
  {
    "demand_sum": 55357.5,
    "material_id": 14,
    "material_name": "Binder 1 (SBR)",
    "percentage_of_current_stock": 55917,
    "unit": "Pcs"
  },
  {
    "demand_sum": 12000.0,
    "material_id": 15,
    "material_name": "Binder 2 (CMC)",
    "percentage_of_current_stock": 12121,
    "unit": "Pcs"
  }
]
```