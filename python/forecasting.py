import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os

print("Starting AI Sales Forecasting & Automated Insight Generation...")

# 1. Load cleaned dataset
df = pd.read_csv('data/cleaned/superstore_cleaned.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

# 2. Aggregate monthly sales and profit
df['year_month'] = df['order_date'].dt.to_period('M').dt.to_timestamp()
monthly_df = df.groupby('year_month').agg({
    'sales': 'sum',
    'profit': 'sum'
}).reset_index().sort_values('year_month')

# 3. Feature Engineering for Time-Series Forecasting
monthly_df['time_index'] = np.arange(len(monthly_df))
monthly_df['month'] = monthly_df['year_month'].dt.month
monthly_df['year'] = monthly_df['year_month'].dt.year

# 4. Train Machine Learning Model (Random Forest Regressor)
features = ['time_index', 'month', 'year']
X = monthly_df[features]
y = monthly_df['sales']

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# Predict on historical data to compare Actual vs Predicted
monthly_df['predicted_sales'] = model.predict(X).round(2)
monthly_df['record_type'] = 'Historical'

# 5. Statistical Anomaly Detection (Z-Score on Residuals)
monthly_df['residual'] = monthly_df['sales'] - monthly_df['predicted_sales']
std_residual = monthly_df['residual'].std()
monthly_df['is_anomaly'] = np.where(
    np.abs(monthly_df['residual']) > (1.75 * std_residual),
    'Anomaly Detected',
    'Normal'
)

# 6. Predict Future 6 Months
last_date = monthly_df['year_month'].max()
last_index = monthly_df['time_index'].max()

future_dates = pd.date_range(
    start=last_date + pd.DateOffset(months=1),
    periods=6,
    freq='MS'
)

future_df = pd.DataFrame({
    'year_month': future_dates,
    'time_index': np.arange(last_index + 1, last_index + 7),
    'month': future_dates.month,
    'year': future_dates.year,
    'sales': np.nan,
    'profit': np.nan
})

future_df['predicted_sales'] = model.predict(future_df[features]).round(2)
future_df['record_type'] = '6-Month Forecast'
future_df['residual'] = np.nan
future_df['is_anomaly'] = 'Future Forecast'

# Combine Historical and Future Forecast
forecast_output = pd.concat([monthly_df, future_df], ignore_index=True)

os.makedirs('data/processed', exist_ok=True)
forecast_path = 'data/processed/sales_forecast.csv'
forecast_output.to_csv(forecast_path, index=False)

# 7. Automated Data-Driven Business Insights Generation
# Calculate real metrics from the dataset
yearly_sales = df.groupby(df['order_date'].dt.year)['sales'].sum()
first_year, last_year = yearly_sales.index.min(), yearly_sales.index.max()
overall_growth = ((yearly_sales[last_year] - yearly_sales[first_year]) / yearly_sales[first_year]) * 100

cat_summary = df.groupby('category').agg({'sales': 'sum', 'profit': 'sum'})
cat_summary['margin'] = (cat_summary['profit'] / cat_summary['sales']) * 100
top_cat = cat_summary['profit'].idxmax()
low_margin_cat = cat_summary['margin'].idxmin()
low_margin_val = cat_summary.loc[low_margin_cat, 'margin']

subcat_loss = df.groupby('sub_category')['profit'].sum()
worst_subcat = subcat_loss.idxmin()
worst_subcat_val = subcat_loss.min()

high_disc_loss = df[df['discount'] >= 0.20]['profit'].sum()
next_6m_total = future_df['predicted_sales'].sum()

insights_data = [
    {
        'Insight_Category': '1. WHAT HAPPENED?',
        'Headline': f'Annual Revenue Grew by {overall_growth:.1f}% ({first_year} to {last_year})',
        'Detailed_Insight': f'Total annual sales expanded from ${yearly_sales[first_year]:,.0f} in {first_year} to ${yearly_sales[last_year]:,.0f} in {last_year}, driven by strong fourth-quarter seasonal demand.',
        'Actionable_Recommendation': 'Scale inventory and warehouse staffing ahead of Q4 (September-December) to prevent stockouts during peak seasonal surges.'
    },
    {
        'Insight_Category': '2. WHY DID IT HAPPEN?',
        'Headline': f'{top_cat} Drives Profit, While {low_margin_cat} Has Low Margin ({low_margin_val:.1f}%)',
        'Detailed_Insight': f'{low_margin_cat} generates strong revenue but suffers from a {low_margin_val:.1f}% profit margin. Specifically, {worst_subcat} resulted in a net loss of ${abs(worst_subcat_val):,.0f}, heavily driven by orders with 20%+ discounts (totaling ${high_disc_loss:,.0f} in profit impact).',
        'Actionable_Recommendation': f'Cap maximum promotional discounts on {low_margin_cat} (especially {worst_subcat}) at 15% and renegotiate supplier unit costs.'
    },
    {
        'Insight_Category': '3. WHAT WILL HAPPEN?',
        'Headline': f'Projected ${next_6m_total:,.0f} Revenue Over Next 6 Months',
        'Detailed_Insight': f'The Random Forest time-series model projects ${next_6m_total:,.0f} in total revenue across the upcoming 6 months, following historical seasonal patterns.',
        'Actionable_Recommendation': 'Use the 6-month monthly forecast as the baseline revenue target for regional sales teams and cash-flow planning.'
    },
    {
        'Insight_Category': '4. WHAT SHOULD THE BUSINESS DO?',
        'Headline': 'Protect Margins & Retain High-Value VIP Customers',
        'Detailed_Insight': 'Eliminating unprofitable discounts on loss-making products and prioritizing High-Value VIP customer retention offers the fastest path to expanding net profit margin.',
        'Actionable_Recommendation': 'Launch a VIP loyalty program for top-tier customers and discontinue or reprice the bottom 10 loss-making products identified on Page 4.'
    }
]

insights_df = pd.DataFrame(insights_data)
insights_path = 'data/processed/ai_business_insights.csv'
insights_df.to_csv(insights_path, index=False)

print(f"Forecast saved to: {forecast_path}")
print(f"Automated Insights saved to: {insights_path}")
print("\n--- SUMMARY OF GENERATED INSIGHTS ---")
for row in insights_data:
    print(f"{row['Insight_Category']}: {row['Headline']}")