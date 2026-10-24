# Technical Project Documentation: AI Business Intelligence Dashboard

## 1. System Architecture & Data Pipeline
This project implements an end-to-end ETL, Machine Learning, and Business Intelligence pipeline:
1. **Ingestion & Cleaning (`python/data_cleaning.py`):** Reads raw retail transactions, standardizes snake_case column headers, parses dates (`order_date`, `ship_date`), removes duplicates, fills missing postal codes, and filters invalid sales/quantities.
2. **Exploratory Data Analysis (`python/eda.py`):** Generates baseline trend charts and identifies loss-making products.
3. **Relational Database (`sql/database.sql` & `sql/analysis.sql`):** Stores cleaned records in a MySQL (`ai_bi`) schema and validates KPI aggregations via SQL queries.
4. **Machine Learning Layer (`python/ai_insights.py` & `python/forecasting.py`):**
   - **Customer Segmentation:** Standardizes customer RFM-style metrics (`sales`, `profit`, `total_orders`) using `StandardScaler` and groups buyers into 3 tiers (`High-Value VIPs`, `Standard Customers`, `Low-Value Customers`) using `KMeans(n_clusters=3)`.
   - **Time-Series Forecasting & Anomaly Detection:** Aggregates monthly sales, trains a `RandomForestRegressor` on time index and seasonal features, flags historical residuals exceeding 1.75 standard deviations as anomalies, and forecasts 6 months ahead.
5. **Semantic Model & BI Layer (`powerbi/AI_Business_Intelligence_Dashboard.pbix`):** Connects MySQL and processed ML outputs in a Star Schema using a custom DAX `DateTable` and centralized `Key Measures` table.

## 2. Star Schema Relationships
- `DateTable[Date]` (1) ➔ `ai_bi superstore_sales[order_date]` (*)
- `ai_customer_segments[customer_id]` (1) ➔ `ai_bi superstore_sales[customer_id]` (*)

## 3. Core DAX Measures Reference
- `Total Revenue = SUM('ai_bi superstore_sales'[sales])`
- `Total Profit = SUM('ai_bi superstore_sales'[profit])`
- `Total Cost = [Total Revenue] - [Total Profit]`
- `Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)`
- `Total Orders = DISTINCTCOUNT('ai_bi superstore_sales'[order_id])`
- `Total Customers = DISTINCTCOUNT('ai_bi superstore_sales'[customer_id])`
- `Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)`
- `Previous Year Revenue = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DateTable[Date]))`
- `YoY Revenue Growth % = DIVIDE([Total Revenue] - [Previous Year Revenue], [Previous Year Revenue], 0)`