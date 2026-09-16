-- Complex Analytics using CTEs and Window Functions
-- Calculate Customer Lifetime Value (CLV) and Purchase Frequency
WITH CustomerMetrics AS (
    SELECT 
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.price + oi.freight_value) AS total_revenue,
        MIN(o.order_purchase_timestamp) AS first_purchase,
        MAX(o.order_purchase_timestamp) AS last_purchase
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT 
    customer_unique_id,
    total_orders,
    total_revenue,
    -- Window function to calculate running total of revenue across the customer base
    SUM(total_revenue) OVER (ORDER BY total_revenue DESC) AS cumulative_revenue,
    -- Calculate days between first and last purchase
    EXTRACT(DAY FROM (last_purchase - first_purchase)) AS customer_lifespan_days
FROM CustomerMetrics
ORDER BY total_revenue DESC;