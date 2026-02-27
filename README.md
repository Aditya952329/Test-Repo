# Blinkit Data Analyst Portfolio Project (1.5 YOE Friendly)

A recruiter-ready end-to-end analytics project designed for a **Data Analyst role at Blinkit**.  
It simulates a quick-commerce business scenario and demonstrates practical skills expected from analysts with ~1–2 years of experience.

## Project Theme
**"Dark Store Performance & 10-Minute Delivery Optimization"**

You will analyze order-level data to answer:
- Which dark stores are underperforming on delivery SLAs?
- How do discounts, stockouts, and cancellations impact margin?
- Which categories and time slots drive repeat customers?
- What actionable levers can improve customer experience and profitability?

## Why this project is recruiter-friendly
- Realistic business KPIs (AOV, fill rate, SLA breach, cancellation rate, contribution margin)
- Mix of **SQL + Python** workflows
- Clean storytelling with measurable recommendations
- Resume-ready bullet points included

## Tech Stack
- Python (standard library: csv, datetime, collections)
- SQL (PostgreSQL-compatible)
- Optional dashboard wireframe (KPI ideas in `dashboards/`)

## Repository Structure

```text
.
├── data/
│   ├── raw/
│   │   └── blinkit_orders_sample.csv
│   └── processed/
│       ├── kpi_summary.csv
│       ├── store_performance.csv
│       └── category_hour_heatmap.csv
├── dashboards/
│   └── dashboard_spec.md
├── reports/
│   ├── final_case_study.md
│   └── resume_bullets.md
├── sql/
│   └── blinkit_case_queries.sql
├── src/
│   ├── generate_sample_data.py
│   └── analyze_blinkit.py
└── requirements.txt
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/generate_sample_data.py
python src/analyze_blinkit.py
```

Generated outputs:
- `reports/final_case_study.md` (business narrative + recommendations)
- Processed KPI tables in `data/processed/`
- Resume bullets in `reports/resume_bullets.md`

## Suggested Interview Pitch (30 sec)

> "I built an end-to-end Blinkit-style dark store analytics case study using SQL and Python. I analyzed SLA breaches, cancellations, and margin leakage across stores, categories, and peak hours. My recommendations targeted high-impact slots and discount inefficiencies, showing how ops and pricing changes can improve both customer experience and contribution margin."

