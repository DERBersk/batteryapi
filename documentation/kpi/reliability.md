# Reliability Calculation

Calculate the reliabilities for suppliers based on historical orders. The data is not returned, but written into the supplier table.

**URL** : `/api/kpi/reliability`

**Method** : `GET`

**Data**: 

```json
{
    
}
```

## Success Response

**Code** : `200 OK`

**Content example**: `Computation Successful!`

## Algorithm

### Algorithm Explanation

The `ReliabilityCalculation` function calculates the reliability of each supplier based on their delivery punctuality. The reliability is determined by comparing the punctual deliveries to the total deliveries for each supplier, adjusted by a predefined threshold. The formula is based on [... et al. (20)](www.google.com)

### Necessary Data

The following data is required for the `ReliabilityCalculation` function to work effectively:

- First of all, Historical Orders of each Supplier is needed, to calculate a reliability index. If no data exists, the value is `None`.
- Second, a threshold needs to be defined in the `config.json` file.

### Formula

The reliability \( R \) is calculated using the following formula:

$$
R = \frac{P}{T} - T_h
$$

where:
- \( P \) is the number of punctual deliveries,
- \( T \) is the total number of deliveries,
- \( T_h \) is the threshold.