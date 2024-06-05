# Delete Base Production Volume

Delete one Base Production Volume via id.

**URL** : `/api/baseproduction/<baseproduction_id>`

**URL Parameters** : `baseproduction_id=[integer]` where `baseproduction_id` is the ID of the Base Production Volume.

**Method** : `DELETE`

**Data** : 

```json
{

}
```

## Responses

#### Success Response

**Condition** : If the Base Production Volume exists.

**Code** : `200 OK`

**Content** : `{'message':'Base Production Volume and associated records deleted successfully'}`

#### Error Responses

**Condition** : If there was no Base Production Volume available to delete.

**Code** : `404 NOT FOUND`

**Content** : `{'error': 'Base Production Volume not found'}`


## Example 

**Call**: `DELETE /api/baseproduction/1`

**Data**:

```json
{

}
```

**Response**: 

`200 OK`

`{'message':'Project and associated records deleted successfully'}`
