# Show total Order Volume over the last year

Show the total number of orders over the last 12 Months

**URL** : `/api/kpi/orderVolume`

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
    "month": "2023-06",
    "total_volume": 12
  },
  {
    "month": "2023-07",
    "total_volume": 3
  },
  ...
]
```