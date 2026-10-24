# AI-Driven Retail Business Intelligence & Forecasting Dashboard

## 📌 Project Overview
An end-to-end **Data Analytics & AI Business Intelligence** portfolio project that transforms raw retail transaction data into an interactive, 5-page executive Power BI dashboard. By combining **Python (Pandas, Scikit-Learn)**, **MySQL**, and **Power BI (Star Schema, DAX)**, this solution diagnoses profit margin leaks, segments customers using unsupervised machine learning, and forecasts future revenue.

---

## 🎯 Business Problem & Objectives
### Business Problem
A national retail company generating over $2.27M in revenue experienced inconsistent profit margins across product categories and lacked visibility into customer lifetime value, discount erosion, and upcoming quarterly demand.

### Core Objectives
1. **Centralize KPI Tracking:** Monitor Revenue, Profit, Cost, Profit Margin %, Order Volume, and Average Order Value (AOV) dynamically across regions and timeframes.
2. **Diagnose Margin Erosion:** Pinpoint specific categories, sub-categories, and individual products causing financial losses.
3. **AI Customer Segmentation:** Automatically group customers by purchasing behavior using K-Means Clustering to guide marketing and retention.
4. **Predictive Sales Forecasting:** Forecast 6-month future sales using a Random Forest time-series model and detect historical revenue anomalies.

---

## 📂 Dataset
- **Source:** Superstore Retail Sales Dataset (Kaggle)
- **Granularity:** Transaction line-item level (~9,994 rows, 21 columns)
- **Key Attributes:** `Order ID`, `Order Date`, `Customer ID`, `Segment`, `Region`, `State`, `Category`, `Sub-Category`, `Product Name`, `Sales`, `Quantity`, `Discount`, `Profit`.

---

## 🛠️ Technology Stack
| Layer | Tools & Libraries | Purpose |
| :--- | :--- | :--- |
| **Data Cleaning & EDA** | Python (`pandas`, `numpy`, `matplotlib`, `seaborn`) | Automated ETL, date parsing, deduplication, and initial visual discovery |
| **Database & Querying** | MySQL, MySQL Workbench | Relational storage, schema enforcement, and SQL business analysis |
| **AI / Machine Learning** | Python (`scikit-learn`) | `KMeans` customer clustering, `RandomForestRegressor` sales forecasting, Z-score anomaly detection |
| **Business Intelligence** | Microsoft Power BI Desktop, DAX, Power Query | Star schema modeling, time-intelligence DAX KPIs, interactive UI design |

---

## 🏗️ Project Architecture
```text
Raw Dataset (CSV) 
  ➔ Python ETL & Cleaning (data_cleaning.py) 
  ➔ MySQL Database Storage & SQL Validation (database.sql, analysis.sql) 
  ➔ Python Machine Learning: K-Means & Random Forest (ai_insights.py, forecasting.py) 
  ➔ Power BI Star Schema & DAX Measures 
  ➔ 5-Page Executive Dashboard & Actionable Recommendations