# 🛒 Supermarket Sales Analysis

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Internship](https://img.shields.io/badge/AICTE--IBM%20SkillsBuild-Internship%202026-orange.svg)](https://skillsbuild.org/)
[![Organization](https://img.shields.io/badge/Organization-BharatCares-green.svg)](https://bharatcares.org/)
[![Tests](https://img.shields.io/badge/Tests-41%20Passed-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## 📋 Project Information

| Parameter | Details |
|---|---|
| **Program** | AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 |
| **Organization** | BharatCares |
| **Project Title** | Supermarket Sales Analysis |
| **Student Name** | Atharav Tayade |
| **Domain** | Data Analytics with AI |
| **Primary Language** | Python (3.9+) |
| **Execution Environment** | Python 3.11.15 / Windows |

---

## 📖 Executive Summary & Problem Statement

Modern supermarket chains face complex challenges in inventory allocation, cashier staffing, loyalty program management, and branch performance optimization. This project performs an end-to-end, reproducible data analytics workflow on historical transaction data from three supermarket branches across three cities in Myanmar (Yangon, Mandalay, and Naypyitaw).

### Key Objectives
1. **Data Ingestion & Integrity**: Ingest, inspect, validate, and clean raw point-of-sale transaction logs.
2. **Exploratory Data Analysis (EDA)**: Evaluate sales volume, customer types, product performance, payment channels, and temporal dynamics.
3. **Statistical & Rating Analysis**: Assess customer satisfaction across branches and product lines.
4. **Machine Learning Pipeline**: Implement an explainable regression model to predict sales totals, benchmarking against baseline models with rigorous discussion of deterministic data constraints.
5. **Business Intelligence & Strategy**: Synthesize evidence-based insights, operational recommendations, and actionable risk limitations.

---

## 📂 Repository Structure

```text
Supermarket-Sales-Analysis/
│
├── AtharavTayade_SupermarketSalesAnalysis.ipynb      # Primary executed Jupyter analysis notebook
├── AtharavTayade_ProjectReport.docx                 # Formal Word internship report (14 figures, 8 tables)
├── requirements.txt                                 # Pinned Python package dependencies
├── README.md                                        # Master repository documentation
├── .gitignore                                       # Git ignore rules for virtualenvs, caches, artifacts
├── generate_report.py                               # Automated DOCX generation script
│
├── data/
│   ├── README.md                                    # Data source details and manual acquisition instructions
│   ├── .gitkeep
│   └── supermarket_sales.csv                        # 1,000 transaction records
│
├── docs/
│   ├── methodology.md                               # Step-by-step analytical methodology
│   └── data_dictionary.md                           # Comprehensive column definitions and data types
│
├── outputs/
│   ├── figures/                                     # 14 high-resolution exported charts (PNG)
│   │   ├── actual_vs_predicted.png
│   │   ├── correlation_heatmap.png
│   │   ├── customer_analysis.png
│   │   ├── daily_sales_trend.png
│   │   ├── day_of_week_sales.png
│   │   ├── feature_importance.png
│   │   ├── hourly_sales.png
│   │   ├── monthly_sales.png
│   │   ├── payment_analysis.png
│   │   ├── rating_by_product_line.png
│   │   ├── rating_distribution.png
│   │   ├── sales_by_branch.png
│   │   ├── sales_by_product_line.png
│   │   ├── sales_distribution.png
│   │   └── txn_count_by_product_line.png
│   └── tables/                                      # Exported analytical summary CSVs
│       ├── summary_metrics.csv
│       ├── business_insights.csv
│       ├── model_comparison.csv
│       ├── sales_by_branch.csv
│       ├── sales_by_product_line.csv
│       └── sales_by_payment.csv
│
├── src/
│   ├── __init__.py                                  # Package initialization
│   ├── data_loader.py                               # Ingestion, schema validation & logging
│   ├── data_cleaning.py                             # Missing values, date parsing & validation
│   ├── analysis.py                                  # KPI calculation, product/branch/time aggregations
│   ├── visualizations.py                            # Matplotlib/Seaborn professional visual generators
│   └── insights.py                                  # Automated structured insight synthesis
│
└── tests/
    ├── test_data_cleaning.py                        # 19 unit tests for cleaning routines & edge cases
    └── test_analysis.py                             # 22 unit tests for KPI calculations & metrics
```

---

## 📊 Dataset Description & Source

- **Name**: Supermarket Sales Dataset
- **Author**: Aung Pyae (2019)
- **Direct Link**: [Kaggle Supermarket Sales Dataset](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)
- **Scope**: Historical record of 1,000 supermarket purchase transactions over 3 months (January 1, 2019 – March 30, 2019).
- **Locations**: Branch A (Yangon), Branch B (Mandalay), Branch C (Naypyitaw).
- **Core Attributes**: Invoice ID, Branch, City, Customer type, Gender, Product line, Unit price, Quantity, Tax 5%, Total, Date, Time, Payment, COGS, Gross margin percentage, Gross income, and Rating.

### Acquisition Instructions
1. Download `supermarket_sales.csv` from [Kaggle](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales).
2. Place the file inside the `data/` directory: `data/supermarket_sales.csv`.
3. If already present in this workspace, the loader reads it automatically.

---

## 🛠️ Technologies & Dependencies

- **Language**: Python 3.9+ (verified on Python 3.11.15)
- **Data Manipulation**: `pandas>=1.5.0`, `numpy>=1.23.0`
- **Visualization**: `matplotlib>=3.6.0`, `seaborn>=0.12.0`
- **Machine Learning**: `scikit-learn>=1.2.0`
- **Interactive Notebook**: `jupyter>=1.0.0`, `notebook>=6.5.0`, `ipykernel>=6.20.0`
- **Report Generation**: `python-docx>=0.8.11`
- **Quality Assurance**: `pytest>=7.2.0`

---

## 🚀 Installation & Reproduction Instructions

### 1. Clone or Open the Repository
```bash
git clone https://github.com/atharavtayade/Supermarket-Sales-Analysis.git
cd Supermarket-Sales-Analysis
```

### 2. Set Up a Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run Unit Tests (41 Tests)
Verify pipeline functionality and edge case handling:
```bash
pytest -v
```
*Expected Result: 41 passed in ~0.5s.*

### 5. Execute Analysis & View Jupyter Notebook
To view or re-run the end-to-end interactive notebook:
```bash
jupyter notebook AtharavTayade_SupermarketSalesAnalysis.ipynb
```
Or execute headlessly from CLI:
```bash
python -m jupyter nbconvert --to notebook --execute AtharavTayade_SupermarketSalesAnalysis.ipynb --output AtharavTayade_SupermarketSalesAnalysis.ipynb
```

### 6. Generate Formal Word Report (.docx)
To regenerate `AtharavTayade_ProjectReport.docx` with fresh charts and tables:
```bash
python generate_report.py
```

---

## 📈 Key Findings & Verified Results

All numbers below are calculated directly from `data/supermarket_sales.csv` (1,000 verified rows):

| Dimension | Metric | Observed Value | Business Implication |
|---|---|---|---|
| **Overall Revenue** | Total Sales | **$322,966.75** | Healthy quarterly turnover across all branches |
| **Transaction Volume** | Total Invoices | **1,000** | Equal transaction volume distribution |
| **Ticket Size** | Average Transaction | **$322.97** (Median: $253.85) | Right-skewed distribution; basket builder opportunities |
| **Quantity** | Total Items Sold | **5,510 units** (Avg: 5.51 units/txn) | Steady basket size per visit |
| **Gross Margin** | Constant Markup | **4.7619%** ($15,379.37 gross profit) | Uniform pricing policy across all categories |
| **Top Product Line** | Food & Beverages | **$56,144.84** (174 transactions) | Highest revenue category; staple demand driver |
| **Lowest Product Line** | Health & Beauty | **$49,193.74** (152 transactions) | Potential for assortment expansion or promotion |
| **Branch Leader** | Branch C (Naypyitaw) | **$110,568.71** (328 txns) | Top performing branch in volume and gross turnover |
| **Branch Comparison** | Branch A (Yangon) / B (Mandalay) | **$106,200.37** / **$106,197.67** | Tight sales parity between Yangon and Mandalay |
| **Customer Type** | Member vs Normal | **$164,223.44** (50.8%) vs **$158,743.30** (49.2%) | Loyalty members spend slightly higher per visit |
| **Payment Channel** | Most Frequent Method | **Ewallet: 345 txns** ($109,993.11) | Digital wallets are preferred over Cash & Credit Card |
| **Peak Shopping Time** | Highest Sales Hour | **19:00 (7 PM)**: $39,699.51 | Critical evening rush requires optimal cashier staffing |
| **Customer Satisfaction**| Average Rating | **6.97 / 10** (Range: 4.0 – 10.0) | Moderate satisfaction with normal distribution |

---

## 🤖 Machine Learning Modeling & Critical Caveats

### Model Overview
A regression task was evaluated using **Random Forest Regressor** to predict transaction totals based on transaction features:
- **Baseline Model (Mean Predictor)**: RMSE = $255.75, MAE = $209.77, R² = -0.0053
- **Random Forest Regressor (100 Trees)**: RMSE = $10.12, MAE = $6.73, R² = 0.9984

### Critical Data Science Disclaimer & Transparency
> **Important Analytical Caveat**:  
> In point-of-sale transaction datasets where total amount is calculated via `Total = (Unit price × Quantity) × 1.05`, predicting `Total` using `Unit price` and `Quantity` is learning an underlying deterministic mathematical relationship rather than stochastic human behavior. While this confirms the algorithmic capability of Random Forest to model non-linear interactions, the primary value of this project lies in descriptive business intelligence and operational diagnosis rather than black-box prediction.

---

## 💡 Strategic Recommendations

1. **Staffing Optimization During Peak Windows**: Staff cashier lanes and customer service desks heavily between **18:00 and 20:00 (peak: 19:00)** to prevent checkout bottlenecking.
2. **Revitalizing Underperforming Categories**: Launch bundle promotions combining high-velocity *Food & Beverages* items with slower-moving *Health & Beauty* items.
3. **Loyalty Program Enhancement**: Strengthen the Member value proposition (currently only 50.8% of sales) through tiered loyalty perks, members-only promotions, and digital wallet cashback partnerships.
4. **Branch Best Practice Transfer**: Transfer operational best practices from Branch C (Naypyitaw) to Branch A and B to close the $4,371 revenue gap.

---

## ⚠️ Analytical Limitations

1. **Short Observation Horizon**: Three months of data (Jan–Mar 2019) does not capture annual seasonality, holiday peaks, or long-term growth.
2. **No Persistent Customer Identifiers**: Transactions are anonymous; repeat visitation rates and Customer Lifetime Value (CLV) cannot be calculated.
3. **Fixed Margin Structure**: The 4.76% gross margin percentage is invariant across all categories, precluding price elasticity and true gross margin variance analysis.
4. **Correlation vs. Causation**: Observational findings represent correlations in historical records and do not establish direct causality.

---

## 📚 References

1. Aung Pyae, *"Supermarket Sales"* dataset, Kaggle (2019). [https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)
2. Wes McKinney, *"pandas: a foundational Python library for data analysis and statistics"*, Python for High Performance and Scientific Computing (2011).
3. Pedregosa, F., et al., *"Scikit-learn: Machine Learning in Python"*, JMLR 12 (2011): 2825-2830.
4. Hunter, J. D., *"Matplotlib: A 2D Graphics Environment"*, Computing in Science & Engineering (2007).
5. Waskom, M., *"seaborn: statistical data visualization"*, Journal of Open Source Software (2021).

---

## 🌐 GitHub Publication Instructions

To publish this project to GitHub under your account:

```bash
# 1. Initialize Git repository
git init

# 2. Add all files
git add .

# 3. Commit initial project files
git commit -m "feat: complete AICTE-IBM SkillsBuild Supermarket Sales Analysis project"

# 4. Create repository on GitHub (via GitHub CLI or web UI)
# Using gh CLI:
# gh repo create Supermarket-Sales-Analysis --public --source=. --remote=origin --push

# Or manually via Git remote:
# git branch -M main
# git remote add origin https://github.com/<your-username>/Supermarket-Sales-Analysis.git
# git push -u origin main
```

---

*Submitted by Atharav Tayade for the AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026 in partnership with BharatCares.*
