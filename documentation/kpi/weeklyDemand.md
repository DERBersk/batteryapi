# Material Demand Calculation

Calculate the material demand based on base production data, project data, and product composition.

**URL** : `/api/kpi/materialDemand`

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
        "material_id": 1,
        "week": "2024-W24",
        "demand": 500
    },
    {
        "material_id": 2,
        "week": "2024-W24",
        "demand": 300
    },
    {
        "material_id": 3,
        "week": "2024-W24",
        "demand": 150
    },
    ...
]
```

## Algorithm

### Algorithm Explanation

The `OptimalOrderCalculation` function determines the optimal order quantities for materials by following these steps:

1. Data Filtering:
    - Filter the base production data to include only records for weeks later than the current week.
    - Filter the project data to include only active projects within the relevant time frame or oncoming Projects

2. Demand Calculation:
    - Calculate the weekly total product demand by summing the demands from the base production data and project data.
    - Calculate the weekly total material demand by mapping the product demand to the required materials using the composition data.

3. Data Storage:
    - Save the calculated material demand data into a new table, updating existing data if necessary.

4. Output Generation:
    - Retrieve and return the stored weekly material demand data as the final output.

### Necessary Data

The following data is required for the `MaterialDemandCalculation` function to work effectively:

   - Weekly production volume data for each product, including details for weeks later than the current week.
   - Data for ongoing and upcoming projects, including project start and end weeks, and the amount of each product required.
   - Relationship data between projects and products, detailing the quantities of products required for each project.
   - Composition data showing which materials are required for each product and in what quantities.