# Blinkit Dark Store Performance Case Study

## 1. Executive Summary
- Analyzed **12,000 orders** across 12 dark stores.
- Cancellation rate: **7.58%**.
- SLA breach rate: **46.97%**.
- Margin on revenue: **77.97%**.

## 2. KPI Snapshot
- **total_orders**: 12000
- **fulfilled_orders**: 11091
- **cancelled_orders**: 909
- **cancellation_rate_pct**: 7.58
- **sla_breach_rate_pct**: 46.97
- **avg_actual_delivery_mins**: 20.11
- **avg_order_value_fulfilled**: 416.46
- **total_revenue**: 4619003.51
- **total_contribution_margin**: 3601236.86
- **margin_pct_on_revenue**: 77.97

## 3. High-Risk Stores
- DS_03 (Hyderabad): SLA 52.0%, Cancel 6.4%, Avg delivery 20.8 mins
- DS_02 (Bengaluru): SLA 51.1%, Cancel 6.6%, Avg delivery 20.6 mins
- DS_01 (Delhi NCR): SLA 51.0%, Cancel 7.3%, Avg delivery 20.7 mins

## 4. Peak Leakage Slots
- Personal Care at 23:00 | Cancel 19.3% | SLA 33.3% | Avg margin 229.33
- Personal Care at 20:00 | Cancel 16.1% | SLA 67.7% | Avg margin 268.76
- Beverages at 19:00 | Cancel 14.5% | SLA 59.2% | Avg margin 296.57
- Dairy & Breakfast at 20:00 | Cancel 14.1% | SLA 69.6% | Avg margin 285.63
- Fruits & Vegetables at 20:00 | Cancel 13.8% | SLA 66.1% | Avg margin 327.98

## 5. Recommendations
1. Add rider buffer for 7 PM to 10 PM in high-risk stores.
2. Launch hourly refill alerts for fast-moving SKUs to reduce stockout cancellations.
3. Rebalance discount strategy away from low-margin, high-cancellation windows.
