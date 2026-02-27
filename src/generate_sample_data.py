import csv
import random
from datetime import datetime, timedelta

random.seed(42)

N_ORDERS = 12000
STORE_IDS = [f"DS_{i:02d}" for i in range(1, 13)]
CITIES = ["Bengaluru", "Mumbai", "Delhi NCR", "Hyderabad"]
CATEGORIES = [
    "Fruits & Vegetables",
    "Dairy & Breakfast",
    "Snacks & Munchies",
    "Beverages",
    "Personal Care",
    "Household",
]
PAYMENT_MODES = ["UPI", "Card", "COD", "Wallet"]


def clamp(value: float, min_v: float, max_v: float) -> float:
    return max(min_v, min(value, max_v))


def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]


def main() -> None:
    start = datetime(2024, 1, 1)
    end = datetime(2024, 3, 31, 23, 59, 59)
    span_seconds = int((end - start).total_seconds())

    header = [
        "order_id",
        "order_ts",
        "city",
        "store_id",
        "customer_id",
        "category",
        "items_count",
        "gross_order_value",
        "discount_amount",
        "fulfilled_order_value",
        "eta_mins",
        "actual_delivery_mins",
        "sla_breached",
        "stockout_flag",
        "cancelled_flag",
        "payment_mode",
        "variable_cost",
        "contribution_margin",
    ]

    with open("data/raw/blinkit_orders_sample.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for i in range(1, N_ORDERS + 1):
            sec = random.randint(0, span_seconds)
            order_ts = start + timedelta(seconds=sec)
            hour = order_ts.hour
            is_peak = hour in (19, 20, 21)

            gross_order_value = random.gammavariate(2.8, 170)
            items_count = max(1, int(random.gauss(6, 2)))

            discount_pct = clamp(random.gauss(12, 6), 0, 35)
            discount_amount = gross_order_value * (discount_pct / 100)

            rainy_penalty = 1 if random.random() < 0.18 else 0
            eta_mins = clamp(round(random.gauss(17, 4.5) + (4 if is_peak else 0) + (6 if rainy_penalty else 0)), 8, 60)
            actual_delivery_mins = clamp(round(eta_mins + random.gauss(1.5, 6)), 6, 90)

            sla_breached = 1 if actual_delivery_mins > 20 else 0
            stockout_prob = 0.09 + (0.08 if is_peak else 0)
            stockout_flag = 1 if random.random() < stockout_prob else 0

            cancel_probability = clamp(0.02 + 0.09 * sla_breached + 0.14 * stockout_flag, 0, 0.55)
            cancelled_flag = 1 if random.random() < cancel_probability else 0

            fulfilled_order_value = 0 if cancelled_flag else gross_order_value - discount_amount

            pick_pack_cost = random.gauss(28, 5)
            last_mile_cost = random.gauss(38, 9) + 0.8 * actual_delivery_mins
            platform_fee = random.gauss(9, 2.5)

            variable_cost = random.gauss(11, 3) if cancelled_flag else (pick_pack_cost + last_mile_cost + platform_fee)
            contribution_margin = fulfilled_order_value - variable_cost

            writer.writerow(
                [
                    f"ORD{i:06d}",
                    order_ts.isoformat(sep=" "),
                    weighted_choice(CITIES, [0.34, 0.26, 0.24, 0.16]),
                    random.choice(STORE_IDS),
                    f"CUST{random.randint(1000, 4500)}",
                    weighted_choice(CATEGORIES, [0.22, 0.18, 0.20, 0.16, 0.12, 0.12]),
                    items_count,
                    round(gross_order_value, 2),
                    round(discount_amount, 2),
                    round(fulfilled_order_value, 2),
                    int(eta_mins),
                    int(actual_delivery_mins),
                    sla_breached,
                    stockout_flag,
                    cancelled_flag,
                    weighted_choice(PAYMENT_MODES, [0.48, 0.24, 0.17, 0.11]),
                    round(variable_cost, 2),
                    round(contribution_margin, 2),
                ]
            )

    print("Generated data/raw/blinkit_orders_sample.csv", N_ORDERS)


if __name__ == "__main__":
    main()
