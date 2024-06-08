# Delete Order

Delete one Order via id.

**URL** : `/api/order/<order_id>`

**URL Parameters** : `order_id=[integer]` where `order_id` is the ID of the Order.

**Method** : `DELETE`

**Data** : 

```json
{

}
```

## Responses

#### Success Response

**Condition** : If the Order exists.

**Code** : `200 OK`

**Content** : `{'message':'Order and associated records deleted successfully'}`

#### Error Responses

**Condition** : If there was no Order available to delete.

**Code** : `404 NOT FOUND`

**Content** : `{'error': 'Order not found'}`


## Example 

**Call**: `DELETE /api/order/1`

**Data**:

```json
{

}
```

**Response**: 

`200 OK`

`{'message':'Order deleted successfully'}`
