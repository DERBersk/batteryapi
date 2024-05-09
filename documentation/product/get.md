# Show Multiple Product

Show data of a All Products.

**URL** : `/api/products/`

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
        "description": "down",
        "id": 1,
        "specification": "play"
    },
    {
        "description": "agent",
        "id": 2,
        "specification": "better"
    },
    ...
]
```

# Show Single Product

Show data of a single Product and its associated Product 

**URL** : `/api/products/<product_id>`

**URL Parameters** : `product_id=[integer]` where `product_id` is the ID of the Product.

**Method** : `GET`

**Data**: 

```json
{

}
```

## Success Response

**Condition** : If Product exists.

**Code** : `200 OK`

**Content example**:

```json
{
    "id": 1,
    "description": "Lithium-Ion Battery Pouch v3",
    "materials": [
        {
            "amount": 28,
            "id": 4,
            "lot_size": 8,
            "name": "Lithium-Ion",
            "safety_stock": 7,
            "stock_level": 59.8
        },
        {
            "amount": 24,
            "id": 2,
            "lot_size": 5,
            "name": "Copper",
            "safety_stock": 8,
            "stock_level": 32
        },
    ],
    "specification": "Pouch"
}
```

## Error Responses

**Condition** : If Product does not exist with `id` of provided `product_id` parameter.

**Code** : `404 NOT FOUND`

**Content** : `{'message': 'Product with id {product_id} not found'}`