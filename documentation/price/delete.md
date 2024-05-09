# Delete Price

Delete one Price via id

**URL** : `/api/price/<price_id>`

**URL Parameters** : `price_id=[integer]` where `price_id` is the ID of the Price.

**Method** : `DELETE`

**Data** : 

```json
{

}
```

## Responses

#### Success Response

**Condition** : If the Price exists.

**Code** : `200 OK`

**Content** : `{'message':'Price deleted successfully'}`

#### Error Responses

**Condition** : If there was no Price available to delete.

**Code** : `404 NOT FOUND`

**Content** : `{'error': 'Price not found'}`


## Example 

**Call**: `DELETE /api/price/1`

**Data**:

```json
{

}
```

**Response**: 

`200 OK`

`{'message':'Price deleted successfully'}`
