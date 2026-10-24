import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("Starting Exploratory Data Analysis...")

# 1. Load the cleaned data
df = pd.read_csv('data/cleaned/superstore_cleaned.csv')

# Convert order_date back to datetime since CSV saves it as text
df['order_date'] = pd.to_datetime(df['order_date'])

# 2. Extract Year and Month for Trend Analysis
df['year_month'] = df['order_date'].dt.to_period('M')

# Create a folder for saving our charts if it doesn't exist
os.makedirs('screenshots', exist_ok=True)

# Set the visual style
sns.set_theme(style="whitegrid")

# --- CHART 1: Monthly Sales Trend ---
plt.figure(figsize=(12, 5))
monthly_sales = df.groupby('year_month')['sales'].sum().reset_index()
monthly_sales['year_month'] = monthly_sales['year_month'].astype(str)
sns.lineplot(data=monthly_sales, x='year_month', y='sales', marker="o", color="blue")
plt.xticks(rotation=90)
plt.title('Total Sales Trend by Month')
plt.xlabel('Month-Year')
plt.ylabel('Total Sales ($)')
plt.tight_layout()
plt.savefig('screenshots/1_monthly_sales_trend.png')
print("Chart 1 saved: Monthly Sales Trend")

# --- CHART 2: Profit by Category ---
plt.figure(figsize=(8, 5))
category_profit = df.groupby('category')['profit'].sum().reset_index()
sns.barplot(data=category_profit, x='category', y='profit', palette="viridis")
plt.title('Total Profit by Category')
plt.xlabel('Category')
plt.ylabel('Total Profit ($)')
plt.tight_layout()
plt.savefig('screenshots/2_profit_by_category.png')
print("Chart 2 saved: Profit by Category")

# --- CHART 3: Top 10 Loss-Making Products ---
plt.figure(figsize=(10, 6))
# Filter products with negative profit, group them, and get the worst 10
loss_products = df[df['profit'] < 0].groupby('product_name')['profit'].sum().reset_index()
top_10_losses = loss_products.sort_values(by='profit', ascending=True).head(10)
sns.barplot(data=top_10_losses, x='profit', y='product_name', palette="Reds_r")
plt.title('Top 10 Loss-Making Products')
plt.xlabel('Total Loss ($)')
plt.ylabel('Product Name')
plt.tight_layout()
plt.savefig('screenshots/3_top_10_loss_making_products.png')
print("Chart 3 saved: Top 10 Loss-Making Products")

# --- BUSINESS METRICS OVERVIEW ---
total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
profit_margin = (total_profit / total_sales) * 100

print("\n--- CRITICAL BUSINESS METRICS ---")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Overall Profit Margin: {profit_margin:.2f}%")
print("EDA Complete. Check the 'screenshots' folder for visualizations.")