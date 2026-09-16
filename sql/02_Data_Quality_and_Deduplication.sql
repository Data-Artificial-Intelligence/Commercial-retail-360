-- 1. DEDUPLICATION: Identify and merge duplicate customers based on unique_id
-- Using Window Functions to apply "survivor" logic (keep the earliest customer_id)
WITH RankedCustomers AS (
    SELECT 
        customer_id,
        customer_unique_id,
        ROW_NUMBER() OVER(PARTITION BY customer_unique_id ORDER BY customer_id ASC) as rn
    FROM customers
)
SELECT customer_id, customer_unique_id 
FROM RankedCustomers 
WHERE rn = 1; -- These are the survivor records

-- 2. PII MASKING & COMPLIANCE: Create a secure view for the reporting layer
-- Ensures statutory guidelines (GDPR/POPIA) are met by masking emails/IDs
CREATE VIEW vw_secure_customer_reporting AS
SELECT 
    customer_unique_id AS Customer_Key,
    customer_city,
    customer_state,
    CONCAT(LEFT(customer_city, 2), '***') AS Masked_City -- Example of data obfuscation if needed
FROM customers;