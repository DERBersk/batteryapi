# Risk Calculation

Calculate and update the risk index for each supplier using country risk data and the supplier's reliability.

**URL** : `/api/kpi/riskindex`

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
[
    {
        "availability": true,
        "country": "Czech Rep.",
        "email": null,
        "external_id": "S8452",
        "id": 35,
        "lat": 49.8682325427443,
        "long": 17.4396431263264,
        "mat_count": 0,
        "name": "Resonac Corporation",
        "order_count": 0,
        "reliability": null,
        "risk_index": 0.0,
        "sustainability_index": null
    },
    {
        "availability": true,
        "country": "Netherlands",
        "email": "dominikeitner@gmail.com",
        "external_id": "S6569",
        "id": 19,
        "lat": 51.2672070528815,
        "long": 4.32847522121213,
        "mat_count": 2,
        "name": "Dupont (Test)",
        "order_count": 0,
        "reliability": null,
        "risk_index": 0.0350877,
        "sustainability_index": 0.0
    },
    ...
]
```

## Algorithm

### Algorithm Explanation

The update_supplier_risk_indices function calculates the risk index for each supplier based on their country's risk index and their reliability. The risk index is determined by applying weights to both the country risk index and the supplier's reliability. The calculated risk index is then written into the risk_index field of the Supplier table in the database.

### Necessary Data

The following data is required for the update_supplier_risk_indices function to work effectively:

##### Options Data:

These are set by the user in the Settings Menu
- risk_index_weight_country_risk: Weight for the country risk index in the overall risk calculation.
- risk_index_weight_reliability: Weight for the reliability index in the overall risk calculation.

##### Supplier Data:

- country: The country code of the supplier.
- reliability: The reliability index of the supplier.

##### Country Risk Data:

- Country risk indices from the CountryRisk function, normalized to a scale between 0 and 1.

### Formula

The risk index $R$ for each supplier is calculated using the following formula:

$R = (W_c*C)+(W_r*S)$

where:

- $W_c$ is the weight for the country risk index.
- $C$ is the normalized country risk index for the supplier's country.
- $W_r$ is the weight for the reliability index.
- $S$ is the supplier's reliability index.

If the supplier's reliability index is not available, the formula simplifies to:

$R=C$

where:

$C$ is the normalized country risk index for the supplier's country.
