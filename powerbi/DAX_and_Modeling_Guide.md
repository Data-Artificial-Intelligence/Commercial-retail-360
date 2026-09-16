# Power BI Semantic Model & DAX Guide

## Data Modeling (Star Schema)
* **Fact Tables:** `fact_orders`, `fact_order_items`
* **Dimension Tables:** `dim_customers`, `dim_products`, `dim_date`
* **Relationships:** 1-to-Many from Dimensions to Facts. Cross-filter direction: Single.

## Key DAX Measures

### 1. Total Revenue
```dax
Total Revenue = 
SUMX(
    fact_order_items, 
    fact_order_items[price] * fact_order_items[quantity]
)
```

### 2. Year-over-Year (YoY) Growth

```dax
Total Revenue LY = 
CALCULATE(
    [Total Revenue], 
    SAMEPERIODLASTYEAR(dim_date[date])
)

YoY Growth % = 
DIVIDE(
    [Total Revenue] - [Total Revenue LY], 
    [Total Revenue LY], 
    0
)

```

### 3. On-Time Delivery SLA Compliance

On-Time Delivery % = 
VAR DeliveredOrders = COUNTROWS(
    FILTER(
        fact_orders, 
        fact_orders[order_delivered_customer_date] <= fact_orders[order_estimated_delivery_date]
    )
)
VAR TotalOrders = COUNTROWS(fact_orders)
RETURN
DIVIDE(DeliveredOrders, TotalOrders, 0)

