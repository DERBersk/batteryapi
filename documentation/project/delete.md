# Delete Projects

Delete one Project via id and associated ProductsPerProjects.

**URL** : `/api/project/<project_id>`

**URL Parameters** : `project_id=[integer]` where `project_id` is the ID of the Project.

**Method** : `DELETE`

**Data** : 

```json
{

}
```

## Responses

#### Success Response

**Condition** : If the Project exists.

**Code** : `200 OK`

**Content** : `{'message':'Project and associated records deleted successfully'}`

#### Error Responses

**Condition** : If there was no Project available to delete.

**Code** : `404 NOT FOUND`

**Content** : `{'error': 'Project not found'}`


## Example 

**Call**: `DELETE /api/project/1`

**Data**:

```json
{

}
```

**Response**: 

`200 OK`

`{'message':'Project and associated records deleted successfully'}`
