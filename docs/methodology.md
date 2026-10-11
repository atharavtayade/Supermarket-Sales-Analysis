# Methodology

## Supermarket Sales Analysis — Analytical Methodology

### 1. Data Collection
- **Source**: Kaggle Supermarket Sales Dataset  
  (https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)
- **Format**: CSV file with 1,000 transaction records
- **Coverage**: Sales transactions from three supermarket branches (January–March 2019)

### 2. Data Quality Assessment
The following checks are performed during data loading:
1. **Schema validation**: Verify expected columns are present
2. **Missing value analysis**: Count and percentage of nulls per column
3. **Duplicate detection**: Identify and remove exact duplicate rows
4. **Data type verification**: Ensure numeric, date, and categorical columns have correct types
5. **Range validation**: Check numerical fields for out-of-range or suspicious values
6. **Categorical validation**: Verify categorical fields contain only expected values

### 3. Data Cleaning & Preprocessing
1. Strip whitespace from column names
2. Remove duplicate records (if any)
3. Parse date and time fields into proper datetime types
4. Extract temporal features: Day, Month, Month_Name, Day_of_Week, Week_Number, Hour
5. Coerce numeric columns to appropriate types
6. Document all cleaning decisions

### 4. Exploratory Data Analysis (EDA)
The EDA follows a structured approach:

#### A. Descriptive Statistics
- Transaction count, total sales, average/median transaction values
- Total quantity sold, total gross income, average rating

#### B. Categorical Analysis
- **Product line**: Sales, transactions, and average values by product category
- **Branch**: Comparative performance across branches A, B, and C
- **Customer type**: Member vs Normal customer segments
- **Gender**: Sales distribution by gender
- **Payment method**: Transaction frequency and sales by payment type

#### C. Temporal Analysis
- **Daily trends**: Time-series of daily sales with moving averages
- **Monthly patterns**: Month-over-month sales performance
- **Day-of-week patterns**: Sales distribution across weekdays
- **Hourly patterns**: Peak and off-peak hours for sales

#### D. Customer Experience
- Rating distribution analysis
- Rating comparisons across product lines, branches, and customer segments

#### E. Correlation Analysis
- Pearson correlation between numerical variables
- Identification of meaningful vs mathematically trivial correlations

### 5. Machine Learning (Optional Enhancement)
- **Task**: Sales amount prediction using regression
- **Model**: Random Forest Regressor with comparison to a baseline (mean prediction)
- **Evaluation**: RMSE, MAE, and R² score on held-out test set
- **Validation**: No target leakage; preprocessing fitted only on training data

### 6. Insights Generation
Each insight follows a structured template:
1. **Finding**: Observed factual result from the analysis
2. **Supporting Metric**: Quantitative evidence
3. **Recommendation**: Actionable business suggestion
4. **Limitation**: Caveats or constraints on the finding

### 7. Tools and Technologies
| Tool | Purpose |
|------|---------|
| Python 3.9+ | Primary programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Matplotlib | Visualization |
| Seaborn | Statistical visualization |
| Scikit-learn | Machine learning |
| Jupyter | Interactive notebook environment |
| python-docx | Report generation |
| Pytest | Unit testing |

### 8. Reproducibility
- Fixed random seed (`RANDOM_SEED = 42`) for all stochastic operations
- Version-pinned dependencies in `requirements.txt`
- Modular source code in `src/` with unit tests in `tests/`
- All results derived from executed code, not manually entered
