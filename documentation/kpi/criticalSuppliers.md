# Show Critical Suppliers for all indexes

Show critical Suppliers, meaning Suppliers that have an index that is in a critical range

**URL** : `/api/kpi/criticalSuppliers`

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
      "reliability": false,
      "risk": true,
      "supplier": {
        "availability": false,
        "country": "China",
        "email": null,
        "external_id": "S9112",
        "id": 11,
        "lat": 35.195581226251,
        "long": 118.265431433867,
        "name": "AME energy Co.,Limited",
        "reliability": 0.8,
        "risk_index": 0.672097,
        "sustainability_index": 0.2
      },
      "sustainability": true
    },
    {
      "reliability": false,
      "risk": true,
      "supplier": {
        "availability": true,
        "country": "United States of America",
        "email": null,
        "external_id": "S2941",
        "id": 15,
        "lat": 35.4187588130353,
        "long": -80.6599928802627,
        "name": "Celgrad",
        "reliability": null,
        "risk_index": 0.66705,
        "sustainability_index": 0.56
      },
      "sustainability": false
    },
  ...
]
```