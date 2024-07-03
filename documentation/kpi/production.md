# Show and Calculate Weekly Production

Calculation based on External Production and Projects (next 10 weeks)

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
      "data": [
        {
          "amount": 0.0,
          "name": "21700-Zelle 4.5 Ah",
          "product_id": 11
        },
        {
          "amount": 0.0,
          "name": "21700-Zelle 4.5 Ah",
          "product_id": 12
        },
        {
          "amount": 0.0,
          "name": "21700-Zelle 4.5 Ah",
          "product_id": 13
        }
      ],
      "week": 24,
      "year": 2024
    },
    {
      "data": [
        {
          "amount": 0.0,
          "name": "21700-Zelle 4.5 Ah",
          "product_id": 11
        },
        {
          "amount": 0.0,
          "name": "21700-Zelle 4.5 Ah",
          "product_id": 12
        },
        {
          "amount": 0.0,
          "name": "21700-Zelle 4.5 Ah",
          "product_id": 13
        }
      ],
      "week": 25,
      "year": 2024
    },
    ...
]
```