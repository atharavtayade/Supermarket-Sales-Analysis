# Data Dictionary

## Supermarket Sales Dataset

**Source**: [Kaggle – Supermarket Sales](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)  
**Records**: 1,000 transactions  
**Time Period**: January – March 2019  
**Branches**: 3 (A, B, C) in Myanmar

---

### Original Columns

| # | Column Name | Data Type | Description | Example Values |
|---|------------|-----------|-------------|----------------|
| 1 | Invoice ID | String | Unique transaction identifier | 750-67-8428 |
| 2 | Branch | Categorical | Supermarket branch code | A, B, C |
| 3 | City | Categorical | City where the branch is located | Yangon, Naypyitaw, Mandalay |
| 4 | Customer type | Categorical | Membership status of the customer | Member, Normal |
| 5 | Gender | Categorical | Customer gender | Male, Female |
| 6 | Product line | Categorical | Product category of the purchased item | Health and beauty, Electronic accessories, Home and lifestyle, Sports and travel, Food and beverages, Fashion accessories |
| 7 | Unit price | Float (USD) | Price per unit of the product | 10.08 – 99.96 |
| 8 | Quantity | Integer | Number of units purchased | 1 – 10 |
| 9 | Tax 5% | Float (USD) | 5% tax on the total cost before tax | Calculated: Unit price × Quantity × 0.05 |
| 10 | Total | Float (USD) | Total price including tax | Calculated: cogs + Tax 5% |
| 11 | Date | Date | Date of purchase | 1/1/2019 – 3/30/2019 |
| 12 | Time | Time | Time of purchase | 10:00 – 20:59 |
| 13 | Payment | Categorical | Payment method used | Cash, Ewallet, Credit card |
| 14 | cogs | Float (USD) | Cost of goods sold (before tax) | Calculated: Unit price × Quantity |
| 15 | gross margin percentage | Float (%) | Gross margin as a percentage | 4.761905 (constant) |
| 16 | gross income | Float (USD) | Gross income from the transaction | Same as Tax 5% |
| 17 | Rating | Float | Customer rating for the shopping experience | 4.0 – 10.0 (scale 1–10) |

---

### Derived Columns (Created During Preprocessing)

| Column Name | Data Type | Description | Source |
|------------|-----------|-------------|--------|
| Day | Integer | Day of the month | Extracted from Date |
| Month | Integer | Month number (1–12) | Extracted from Date |
| Month_Name | String | Full month name | Extracted from Date |
| Day_of_Week | String | Day name (Monday–Sunday) | Extracted from Date |
| Week_Number | Integer | ISO week number | Extracted from Date |
| Hour | Integer | Hour of the transaction (24h) | Extracted from Time |

---

### Key Relationships

- `Total = cogs + Tax 5%`
- `cogs = Unit price × Quantity`
- `Tax 5% = cogs × 0.05`
- `gross income = Tax 5%` (identical values)
- `gross margin percentage` is constant at 4.761905% across all records

### Notes

1. The `gross margin percentage` column is constant for all records, providing limited analytical value.
2. `Total`, `cogs`, `Tax 5%`, and `gross income` are mathematically derived from `Unit price` and `Quantity`, so high correlations among them are expected and not independently informative.
3. `Rating` appears to be independent of sales amounts.
