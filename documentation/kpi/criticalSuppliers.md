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
{
  "reliability": [
    {
      "availability": false,
      "country": "China",
      "email": null,
      "id": 11,
      "lat": 35.195581226251,
      "long": 118.265431433867,
      "name": "AME energy Co.,Limited",
      "reliability": -0.1,
      "risk_index": 0.76722545748501,
      "sustainability_index": 0.899024302173073
    },
    ...
  ],
  "risk": [
    {
      "availability": true,
      "country": "Germany",
      "email": null,
      "id": 17,
      "lat": 52.9063952752977,
      "long": 9.66385927388883,
      "name": "DDP Specialty Products GmbH & Co. KG",
      "reliability": null,
      "risk_index": 0.700980868468645,
      "sustainability_index": 0.525231594912317
    },
    ...
  ],
  "sustainability": [
    {
      "availability": true,
      "country": "France",
      "email": "nourashraf225@gmail.com",
      "id": 12,
      "lat": 47.1985431981444,
      "long": -1.58932183135905,
      "name": "Armor Battery Films",
      "reliability": -0.3,
      "risk_index": 0.251099950171836,
      "sustainability_index": 0.22483555123122
    },
    ...
  ]
}
```