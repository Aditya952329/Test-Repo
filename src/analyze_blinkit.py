import csv
from collections import defaultdict
from datetime import datetime

INPUT_FILE = "data/raw/blinkit_orders_sample.csv"


def pct(num: float, den: float) -> float:
    return 0.0 if den == 0 else (num / den) * 100


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main() -> None:
    rows = []
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["order_ts"] = datetime.fromisoformat(r["order_ts"])
            for k in [
                "gross_order_value",
                "discount_amount",
                "fulfilled_order_value",
                "variable_cost",
                "contribution_margin",
            ]:
                r[k] = float(r[k])
            for k in ["eta_mins", "actual_delivery_mins", "sla_breached", "stockout_flag", "cancelled_flag"]:
                r[k] = int(r[k])
            rows.append(r)

    total_orders = len(rows)
    fulfilled_orders = sum(1 for r in rows if r["cancelled_flag"] == 0)
    cancelled_orders = total_orders - fulfilled_orders
    total_revenue = sum(r["fulfilled_order_value"] for r in rows)
    total_margin = sum(r["contribution_margin"] for r in rows)

    avg_delivery = sum(r["actual_delivery_mins"] for r in rows) / total_orders
    avg_sla_breach = sum(r["sla_breached"] for r in rows) / total_orders
    avg_cancellation = sum(r["cancelled_flag"] for r in rows) / total_orders
    avg_order_value_fulfilled = (
        sum(r["fulfilled_order_value"] for r in rows if r["cancelled_flag"] == 0) / fulfilled_orders
    )

    kpis = {
        "total_orders": total_orders,
        "fulfilled_orders": fulfilled_orders,
        "cancelled_orders": cancelled_orders,
        "cancellation_rate_pct": round(avg_cancellation * 100, 2),
        "sla_breach_rate_pct": round(avg_sla_breach * 100, 2),
        "avg_actual_delivery_mins": round(avg_delivery, 2),
        "avg_order_value_fulfilled": round(avg_order_value_fulfilled, 2),
        "total_revenue": round(total_revenue, 2),
        "total_contribution_margin": round(total_margin, 2),
        "margin_pct_on_revenue": round(pct(total_margin, total_revenue), 2),
    }

    store_groups = defaultdict(list)
    heatmap_groups = defaultdict(list)

    for r in rows:
        store_groups[(r["city"], r["store_id"])].append(r)
        heatmap_groups[(r["category"], r["order_ts"].hour)].append(r)

    store_perf = []
    for (city, store_id), grp in store_groups.items():
        n = len(grp)
        store_perf.append(
            [
                city,
                store_id,
                n,
                sum(x["cancelled_flag"] for x in grp) / n,
                sum(x["sla_breached"] for x in grp) / n,
                sum(x["actual_delivery_mins"] for x in grp) / n,
                sum(x["fulfilled_order_value"] for x in grp),
                sum(x["contribution_margin"] for x in grp),
            ]
        )

    store_perf.sort(key=lambda x: (x[4], x[3]), reverse=True)

    heatmap = []
    for (category, hour), grp in heatmap_groups.items():
        n = len(grp)
        heatmap.append(
            [
                category,
                hour,
                n,
                sum(x["sla_breached"] for x in grp) / n,
                sum(x["cancelled_flag"] for x in grp) / n,
                sum(x["contribution_margin"] for x in grp) / n,
            ]
        )

    top_leakage = sorted(heatmap, key=lambda x: (x[4], x[3]), reverse=True)[:5]

    write_csv("data/processed/kpi_summary.csv", list(kpis.keys()), [list(kpis.values())])
    write_csv(
        "data/processed/store_performance.csv",
        [
            "city",
            "store_id",
            "orders",
            "cancellation_rate",
            "sla_breach_rate",
            "avg_delivery_mins",
            "revenue",
            "contribution_margin",
        ],
        store_perf,
    )
    write_csv(
        "data/processed/category_hour_heatmap.csv",
        ["category", "order_hour", "orders", "sla_breach_rate", "cancellation_rate", "avg_margin"],
        heatmap,
    )

    with open("reports/final_case_study.md", "w", encoding="utf-8") as f:
        f.write("# Blinkit Dark Store Performance Case Study\n\n")
        f.write("## 1. Executive Summary\n")
        f.write(f"- Analyzed **{total_orders:,} orders** across 12 dark stores.\n")
        f.write(f"- Cancellation rate: **{kpis['cancellation_rate_pct']}%**.\n")
        f.write(f"- SLA breach rate: **{kpis['sla_breach_rate_pct']}%**.\n")
        f.write(f"- Margin on revenue: **{kpis['margin_pct_on_revenue']}%**.\n\n")
        f.write("## 2. KPI Snapshot\n")
        for k, v in kpis.items():
            f.write(f"- **{k}**: {v}\n")

        f.write("\n## 3. High-Risk Stores\n")
        for row in store_perf[:3]:
            f.write(
                f"- {row[1]} ({row[0]}): SLA {row[4]*100:.1f}%, Cancel {row[3]*100:.1f}%, Avg delivery {row[5]:.1f} mins\n"
            )

        f.write("\n## 4. Peak Leakage Slots\n")
        for row in top_leakage:
            f.write(
                f"- {row[0]} at {int(row[1]):02d}:00 | Cancel {row[4]*100:.1f}% | SLA {row[3]*100:.1f}% | Avg margin {row[5]:.2f}\n"
            )

        f.write("\n## 5. Recommendations\n")
        f.write("1. Add rider buffer for 7 PM to 10 PM in high-risk stores.\n")
        f.write("2. Launch hourly refill alerts for fast-moving SKUs to reduce stockout cancellations.\n")
        f.write("3. Rebalance discount strategy away from low-margin, high-cancellation windows.\n")

    with open("reports/resume_bullets.md", "w", encoding="utf-8") as f:
        f.write("# Resume-Ready Bullets\n\n")
        f.write(
            f"- Built an end-to-end quick-commerce analytics project using SQL + Python across {total_orders:,} orders and 12 dark stores.\n"
        )
        f.write(
            "- Designed KPI framework for SLA breach, cancellation, and contribution margin to identify high-leakage store-hour segments.\n"
        )
        f.write(
            "- Recommended operational and pricing interventions to improve delivery reliability and profitability.\n"
        )

    print("Analysis complete. Outputs saved in data/processed and reports/.")


if __name__ == "__main__":
    main()
