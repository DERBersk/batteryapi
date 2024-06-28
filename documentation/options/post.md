# Create or Modify Option Strategies

**URL** : `/api/options/strategies`

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

# Create or Modify Option Weights

Updates the weights in the Options table, excluding the strategy field. This endpoint allows you to update the following fields:

**URL** : `/api/options/weights`

**Method** : `POST`

```json
{
    "overall_risk_weight_risk": 0.35,
    "risk_index_weight_reliability": 0.40
}
```

## Success Response

**Code** : `201 CREATED`

**Content example**: `{'message': 'Options updated successfully'}`