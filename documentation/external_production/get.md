# Show Multiple External Production Data

Show data of a All External Productions.

**URL** : `/api/externalproduction/`

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
        "amount": 200.0,
        "id": 1,
        "product_id": 11,
        "week": 24,
        "year": 2024
    },
    {
        "amount": 500.0,
        "id": 2,
        "product_id": 12,
        "week": 24,
        "year": 2024
    },
    {
        "amount": 300.0,
        "id": 3,
        "product_id": 11,
        "week": 25,
        "year": 2024
    },
    {
        "amount": 150.0,
        "id": 4,
        "product_id": 12,
        "week": 25,
        "year": 2024
    },
    {
        "amount": 1000.0,
        "id": 5,
        "product_id": 11,
        "week": 1,
        "year": 2025
    }
]
```

