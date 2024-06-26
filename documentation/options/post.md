# Create or Modify Options

**URL** : `/api/options/`

**Method** : `POST`

**Comment** : The Enum "strategy" can be one of 5 values: "Sustainability","Risk","Lead Time","Price"," "

```json
{
    "strategy":"Sustainability"
}
```

## Success Response

**Code** : `201 CREATED`

**Content example**: `{'message': 'Options updated successfully'}`

## Error Responses

### 400 Bad Request

**Condition** : The strategy is not unter the given 5 Enum categories

**Code** : `400 BAD REQUEST`

**Content** : 

`{'error': 'Invalid strategy name'}`