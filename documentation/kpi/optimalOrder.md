# Optimal Order Calculation

Calculate the optimal order quantities for materials based on various strategies.

**URL** : `/api/kpi/optimalOrders`

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
        "order_needed": true,
        "strategy": "Price",
        "min_order": 50,
        "supplier_id": 3,
        "lead_time": 7,
        "sustainability_index": 0.75,
        "risk_index": 0.2,
        "price": 15.0
    },
    {
        "material_id": 2,
        "order_needed": false,
        "strategy": "Sustainability",
        "min_order": 0,
        "supplier_id": 1,
        "lead_time": 10,
        "sustainability_index": 0.9,
        "risk_index": 0.1,
        "price": 12.5
    },
    {
        "material_id": 3,
        "order_needed": true,
        "strategy": "LeadTime",
        "min_order": 30,
        "supplier_id": 5,
        "lead_time": 5,
        "sustainability_index": 0.6,
        "risk_index": 0.3,
        "price": 20.0
    },
    ...
]
```

## Algorithm

### Algorithm Explanation

The `OptimalOrderCalculation` function determines the optimal order quantities for materials by following these steps:

1. **Strategy Determination**:
   - For each material, the algorithm determines which strategy to use for selecting a supplier. The strategy could focus on sustainability, risk, price, or lead time.

2. **Supplier Selection**:
   - Based on the chosen strategy, the function selects the most appropriate supplier for each material. For example, it might choose the supplier with the highest sustainability score, the lowest risk, the lowest price, or the shortest lead time.

3. **Demand Calculation**:
   - The function calculates the total demand for each material by considering future demand and adding a safety stock buffer.

4. **Order Recommendation**:
   - The algorithm compares the total demand with the current stock level. If the stock is insufficient to meet the demand, it calculates the minimum order quantity needed to cover the shortfall.

5. **Output Generation**:
   - Finally, the function compiles a list of recommended orders, detailing which materials need to be ordered, the quantity needed, and the supplier to be used.

This process ensures efficient material ordering by considering various strategic factors, thereby minimizing costs, risks, or environmental impact while maintaining sufficient inventory levels.

### Necessary Data

The following data is required for the `OptimalOrderCalculation` function to work effectively:

   - All materials in the inventory, including details such as stock level and safety stock.
   - Global options, including the default strategy to use if no material-specific strategy is provided.
   - All suppliers available, including their sustainability index, risk index, and other relevant attributes.
   - Current prices for all materials from all suppliers, with details about the cost and validity period.
   - Relationships between materials and suppliers, including lead times for each supplier-material pair.
   - Forecasted weekly demand for each material fetched from the `MaterialDemandCalculation`.
