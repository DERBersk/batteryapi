# Show and Calculate Weekly Production

Calculation based on Baseline Production and Projects

**URL** : `/api/kpi/production`

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
    "amount": 300.0,
    "product_id": 11,
    "week": 24,
    "year": 2024
  },
  {
    "amount": 500.0,
    "product_id": 12,
    "week": 24,
    "year": 2024
  },
  {
    "amount": 400.0,
    "product_id": 11,
    "week": 25,
    "year": 2024
  },
  {
    "amount": 150.0,
    "product_id": 12,
    "week": 25,
    "year": 2024
  },
  ...
]
```