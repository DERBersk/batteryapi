# Delete Materials

Delete one Material via id and associated Prices, MaterialsPerSupplier and MaterialsPerProduct

**URL** : `/api/materials/<material_id>`

**URL Parameters** : `material_id=[integer]` where `material_id` is the ID of the Material.

**Method** : `DELETE`

**Data** : 

```json
{

}
```

## Responses

#### Success Response

**Condition** : If the Material exists.

**Code** : `200 OK`

**Content** : `{'message':'Material and associated records deleted successfully'}`

#### Error Responses

**Condition** : If there was no Material available to delete.

**Code** : `404 NOT FOUND`

**Content** : `{'error': 'Material not found'}`


## Example 

**Call**: `DELETE /api/materials/1`

**Data**:

```json
{

}
```

**Response**: 

`200 OK`

`{'message':'Material and associated records deleted successfully'}`
