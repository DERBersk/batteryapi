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
{
   "wk26_2024": [
      {
         "lead_time": 2,
         "material_id": 11,
         "min_order": 19351.0,
         "name": "Anodenmaterial (Solid content 50%)",
         "price": 7.0,
         "risk_index": 0.691806793403764,
         "strategy": "Price",
         "supplier_id": 13,
         "supplier_name": "BASF",
         "sustainability_index": 0.825091751085014,
         "unit": null
      },
      {
         "lead_time": 5,
         "material_id": 12,
         "min_order": 48251.0,
         "name": "Graphit",
         "price": 20.0,
         "risk_index": 0.934643063966633,
         "strategy": "Sustainability",
         "supplier_id": 14,
         "supplier_name": "BTR",
         "sustainability_index": 0.614823391587686,
         "unit": null
      },
      {
         "lead_time": 2,
         "material_id": 13,
         "min_order": 661.0,
         "name": "Leitadditiv",
         "price": 50.0,
         "risk_index": 0.765437063720187,
         "strategy": "Price",
         "supplier_id": 16,
         "supplier_name": "Cuircuit Foil",
         "sustainability_index": 0.550682969673082,
         "unit": null
      },
      {
         "lead_time": 4,
         "material_id": 14,
         "min_order": 2401.0,
         "name": "Binder 1 (SBR)",
         "price": 2.0,
         "risk_index": 0.934643063966633,
         "strategy": "Price",
         "supplier_id": 14,
         "supplier_name": "BTR",
         "sustainability_index": 0.614823391587686,
         "unit": null
      }
   ],
   "wk27_2024": [],
   "wk28_2024": [],
   "wk29_2024": [],
   "wk30_2024": [
      {
         "lead_time": 2,
         "material_id": 15,
         "min_order": 401.0,
         "name": "Binder 2 (CMC)",
         "price": 2.99,
         "risk_index": 0.934643063966633,
         "strategy": "Price",
         "supplier_id": 14,
         "supplier_name": "BTR",
         "sustainability_index": 0.614823391587686,
         "unit": null
      }
   ]
}
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

The combination of weekly material demand calculation and optimal order calculation is based on the Network Heuristic from [... et al. (20)](www.google.com)

### Necessary Data

The following data is required for the `OptimalOrderCalculation` function to work effectively:

   - All materials in the inventory, including details such as stock level and safety stock.
   - Global options, including the default strategy to use if no material-specific strategy is provided.
   - All suppliers available, including their sustainability index, risk index, and other relevant attributes.
   - Current prices for all materials from all suppliers, with details about the cost and validity period.
   - Relationships between materials and suppliers, including lead times for each supplier-material pair.
   - Forecasted weekly demand for each material fetched from the `MaterialDemandCalculation`.
   - Upcoming Orders either input manually or through the WMS or ERP Connection Setup
