# Show Products without BOM Data

Show Products without any allocated Materials

**URL** : `/api/kpi/productsWithoutMaterials`

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
    "count": 12,
    "data": [
        {
        "description": "Pouch-Zelle 50 Ah",
        "external_id": "P1235",
        "id": 14,
        "specification": "3.0V"
        },
        {
        "description": "Prism.-Zelle 70 Ah",
        "external_id": "P2095",
        "id": 19,
        "specification": "2.9V"
        },
        {
        "description": "Pouch-Zelle 50 Ah",
        "external_id": "P2108",
        "id": 23,
        "specification": "2.9V"
        },
        {
        "description": "Pouch-Zelle 50 Ah",
        "external_id": "P3214",
        "id": 22,
        "specification": "2.8V"
        },
        {
        "description": "Pouch-Zelle 50 Ah",
        "external_id": "P3666",
        "id": 21,
        "specification": "3.0V"
        },
        {
        "description": "Pouch-Zelle 50 Ah",
        "external_id": "P4242",
        "id": 20,
        "specification": "4.2V"
        },
        {
        "description": "Prism.-Zelle 70 Ah",
        "external_id": "P5277",
        "id": 18,
        "specification": "2.8V"
        },
        {
        "description": "Prism.-Zelle 70 Ah",
        "external_id": "P5397",
        "id": 17,
        "specification": "4.4V"
        },
        {
        "description": "Prism.-Zelle 70 Ah",
        "external_id": "P5488",
        "id": 24,
        "specification": "4.4V"
        },
        {
        "description": "Pouch-Zelle 50 Ah",
        "external_id": "P7942",
        "id": 16,
        "specification": "2.9V"
        },
        {
        "description": "Pouch-Zelle 50 Ah",
        "external_id": "P9991",
        "id": 15,
        "specification": "2.8V"
        },
        {
        "description": "New Product Test",
        "external_id": null,
        "id": 26,
        "specification": "2.8v"
        }
    ]
}
```