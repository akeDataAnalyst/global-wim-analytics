# Global Warehousing & Inventory Analytics Dashboard

This project simulate realistic data flows, cleaning, KPI development, risk scoring, and interactive visualization for a decentralized humanitarian logistics network.

## Project Highlights

- Multi-country humanitarian inventory dataset generation (Ethiopia, Yemen, Bangladesh, South Sudan, Afghanistan)
- Professional data pipeline: generation → cleaning → enrichment → analytics → dashboard
- Composite risk scoring combining expiry pressure, stock availability, and compliance status
- Interactive Streamlit dashboard with filters, KPIs, visualizations, data upload simulation, and audit-ready report export

## Key Results

**Global KPIs**

| Metric                              | Value     | Insight                                                                 |
|-------------------------------------|-----------|-------------------------------------------------------------------------|
| Total Items                         | 1,500     | Multi-country                         |
| Total Current Stock                 | 2,687,965 | Substantial prepositioned volume                                        |
| Average Risk Score (0–100)          | 24.7      | Moderate overall risk; significant tail of high-risk items              |
| % Expired                           | 31.6%     | Realistic expiry rate for protracted crises with access & pipeline issues |
| % Stockout                          | 0.0%      | Strong prepositioning performance                                       |
| % High Priority or Immediate Action | 14.0%     | Items requiring urgent attention                                        |
| % Non-Compliant                     | 16.1%     | Compliance flags reflecting donor/audit challenges                      |
| Average Days on Hand                | 118 days  | 4-month buffer — good readiness with expiry risk                       |

**Country-Level KPI Summary**

| Country       | Items | Stock    | Avg Risk | % Expired | % Near Expiry (<90d) | % Non-Compliant | Avg Days on Hand |
|---------------|-------|----------|----------|-----------|----------------------|-----------------|------------------|
| Afghanistan   | 176   | 321,231  | 26.3     | 30.7%     | 11.9%                | 30.7%           | 118.9            |
| Bangladesh    | 217   | 374,431  | 22.6     | 32.7%     | 12.4%                | 0.0%            | 119.4            |
| Ethiopia      | 462   | 821,562  | 23.0     | 32.0%     | 15.8%                | 0.0%            | 119.0            |
| South Sudan   | 280   | 508,496  | 25.9     | 31.4%     | 12.9%                | 28.6%           | 116.4            |
| Yemen         | 365   | 662,245  | 26.4     | 31.0%     | 14.5%                | 29.6%           | 116.7            |

**Main Insights**  
- Highest combined risk in Yemen and Afghanistan (driven by non-compliance + expiry)  
- Highest near-term expiry pressure in Ethiopia (15.8% items <90 days remaining)  
- Persistent 31–33% expiry rate across all countries → distribution bottlenecks  
- No stockouts and consistent 4-month coverage → effective prepositioning strategy

## Tech Stack

- Python 3.9+
- Streamlit (interactive dashboard)
- Pandas (data cleaning & aggregation)
- Plotly (interactive visualizations)
- NumPy (numerical operations)
- Jupyter Notebooks (phased development)

global-wim-analytics


