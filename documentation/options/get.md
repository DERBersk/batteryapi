# Show the set Strategies

Show the Strategies

**URL** : `/api/options/strategies`

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
{
    "strategy": "Price"
}
```

# Retrieve Options Weights

Retrieves the current weights in the Options table, excluding the strategy field.

**URL** : `/api/options/weights/`

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
{
    "overall_risk_weight_risk": 0.25,
    "overall_risk_weight_sustainability": 0.75,
    "risk_index_weight_country_risk": 0.20,
    "risk_index_weight_reliability": 0.80
}
```