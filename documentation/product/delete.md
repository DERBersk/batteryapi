# Delete Product

Delete one Material via id and associated MaterialsPerProduct and ProductsPerProject

**URL** : `/api/product/<product_id>`

**URL Parameters** : `product_id=[integer]` where `product_id` is the ID of the Product.

**Method** : `DELETE`

**Data** : 

```json
{

}
```

## Responses

#### Success Response

**Condition** : If the Product exists.

**Code** : `200 OK`

**Content** : `{'message':'Product and associated records deleted successfully'}`

#### Error Responses

**Condition** : If there was no Product available to delete.

**Code** : `404 NOT FOUND`

**Content** : `{'error': 'Product not found'}`


## Example 

**Call**: `DELETE /api/product/1`

**Data**:

```
{

}
```

**Response**: 

`200 OK`

`{'message':'Product and associated records deleted successfully'}`
