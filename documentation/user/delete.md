# Delete Users

Delete one User via id.

**URL** : `/api/user/<user_id>`

**URL Parameters** : `user_id=[integer]` where `user_id` is the ID of the User.

**Method** : `DELETE`

**Data** : 

```json
{

}
```

## Responses

#### Success Response

**Condition** : If the User exists.

**Code** : `200 OK`

**Content** : `{'message':'User deleted successfully'}`

#### Error Responses

**Condition** : If there was no User available to delete.

**Code** : `404 NOT FOUND`

**Content** : `{'error': 'User not found'}`


## Example 

**Call**: `DELETE /api/user/1`

**Data**:

```json
{

}
```

**Response**: 

`200 OK`

`{'message':'User deleted successfully'}`
