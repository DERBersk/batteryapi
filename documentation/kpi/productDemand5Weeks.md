# Show Product Demands accumulated over the next 5 weeks

**URL** : `/api/kpi/productDemand5Weeks`

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
        "demand_sum": 18452.5,
        "description": "21700-Zelle 4.5 Ah",
        "percentage_of_total_output": 96,
        "product_id": 11,
        "specification": "2.8V"
    },
    {
        "demand_sum": 150.0,
        "description": "21700-Zelle 4.5 Ah",
        "percentage_of_total_output": 1,
        "product_id": 12,
        "specification": "2.9V"
    },
    {
        "demand_sum": 600.0,
        "description": "21700-Zelle 4.5 Ah",
        "percentage_of_total_output": 3,
        "product_id": 13,
        "specification": "4.2V"
    }
]
```