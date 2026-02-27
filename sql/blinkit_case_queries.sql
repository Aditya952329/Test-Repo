-- Blinkit Data Analyst Portfolio Project SQL Queries
-- Assumes a table name: blinkit_orders

-- 1) Core KPI snapshot
SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN cancelled_flag = 0 THEN 1 ELSE 0 END) AS fulfilled_orders,
    SUM(CASE WHEN cancelled_flag = 1 THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(100.0 * AVG(cancelled_flag), 2) AS cancellation_rate_pct,
    ROUND(100.0 * AVG(sla_breached), 2) AS sla_breach_rate_pct,
    ROUND(AVG(actual_delivery_mins), 2) AS avg_actual_delivery_mins,
    ROUND(SUM(fulfilled_order_value), 2) AS total_revenue,
    ROUND(SUM(contribution_margin), 2) AS total_contribution_margin,
    ROUND(100.0 * SUM(contribution_margin) / NULLIF(SUM(fulfilled_order_value), 0), 2) AS margin_pct_on_revenue
FROM blinkit_orders;

-- 2) Store-level performance leaderboard (worst first)
SELECT
    city,
    store_id,
    COUNT(*) AS orders,
    ROUND(100.0 * AVG(cancelled_flag), 2) AS cancellation_rate_pct,
    ROUND(100.0 * AVG(sla_breached), 2) AS sla_breach_rate_pct,
    ROUND(AVG(actual_delivery_mins), 2) AS avg_delivery_mins,
    ROUND(SUM(fulfilled_order_value), 2) AS revenue,
    ROUND(SUM(contribution_margin), 2) AS contribution_margin
FROM blinkit_orders
GROUP BY city, store_id
ORDER BY sla_breach_rate_pct DESC, cancellation_rate_pct DESC;

-- 3) Category x hour demand and leakage heatmap
SELECT
    category,
    EXTRACT(HOUR FROM order_ts) AS order_hour,
    COUNT(*) AS orders,
    ROUND(100.0 * AVG(sla_breached), 2) AS sla_breach_rate_pct,
    ROUND(100.0 * AVG(cancelled_flag), 2) AS cancellation_rate_pct,
    ROUND(AVG(contribution_margin), 2) AS avg_margin_per_order
FROM blinkit_orders
GROUP BY category, EXTRACT(HOUR FROM order_ts)
ORDER BY cancellation_rate_pct DESC, sla_breach_rate_pct DESC;

-- 4) Customer repeat behavior
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(*) AS order_count,
        SUM(fulfilled_order_value) AS net_spend
    FROM blinkit_orders
    WHERE cancelled_flag = 0
    GROUP BY customer_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_customer_pct,
    ROUND(AVG(net_spend), 2) AS avg_customer_spend
FROM customer_orders;
