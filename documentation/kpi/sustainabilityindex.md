# Sustainability Calculation

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

The following data is required for the Risk Calculation function to work effectively:

##### MaterialsPerSupplier Data:

- co2_emissions: The CO2 emissions associated with the material from the supplier.
- distance: The distance associated with the material from the supplier.

### Formulas

#### Normalization Formula

The normalized value $N$ is calculated using the following formula:

$$
N = \frac{V-V_min}{V_min-V_max}
$$

where:

- $V$ is the value to be normalized.
- $V_min$ is the minimum value in the dataset.
- $V_max$ is the maximum value in the dataset.

If $V_max = V_min$, the normalized value $N$ is set to 0 to avoid division by zero.

#### Euclidean Norm

The Euclidean norm $G$ of a vector $V$ with components $(v_1,v_2,...,v_n)$ is calculated using the formula:

$$
G = \sqrt{v_1^2+v_2^2+...+v_n^2}
$$

This function computes the square root of the sum of squares of all elements in the input values list.

#### Green Value Calculation

The green value $G$ is calculated using the Euclidean norm based on the normalized CO2 emissions and distances for materials supplied by each supplier.

The green value $G$ for a supplier is computed using the Euclidean norm formula:

$$
G = \sqrt{(Average Normalized CO2 Emissions)^2+(Average Normalized Distance)^2}
$$

where:

- $Average Normalized CO2 Emissions$ is the average of normalized CO2 emissions associated with materials supplied by the supplier.
- $Average Normalized Distance$ is the average of normalized transportation distances associated with materials supplied by the supplier.

#### Sustainability Index Calculation

The sustainability index $S$ for each supplier is calculated using the following formula:

$$
S = \frac{1}{\sqrt{2}}*Green Value
$$

where:

- $Green Value$ is the Euclidean norm calculated based on the normalized CO2 emissions and distances for the supplier's materials.