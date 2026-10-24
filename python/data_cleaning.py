import pandas as pd
import os

print("Starting Data Cleaning Process...")

# 1. Load the raw dataset
# Using relative path assuming we run this from the main project folder
file_path = 'data/raw/superstore_sales.csv'
df = pd.read_csv(file_path, encoding='windows-1252')
initial_rows = df.shape[0]

# 2. Standardize Column Names
# Convert to lowercase and replace spaces with underscores for easier SQL querying later
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

# 3. Fix Incorrect Data Types (Dates)
# The dataset has 'order_date' and 'ship_date' as text. We must convert them to datetime.
df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce')
df['ship_date'] = pd.to_datetime(df['ship_date'], format='%m/%d/%Y', errors='coerce')

# 4. Handle Duplicates
duplicates_count = df.duplicated().sum()
df = df.drop_duplicates()

# 5. Handle Missing Values
missing_values = df.isnull().sum()
# In Superstore, 'postal_code' sometimes has nulls. We can fill them with a placeholder or '00000'
df['postal_code'] = df['postal_code'].fillna(0).astype(int)

# 6. Check for Invalid Values (e.g., negative sales or quantity)
invalid_sales = len(df[df['sales'] <= 0])
invalid_quantity = len(df[df['quantity'] <= 0])
# We will drop rows where sales or quantity is 0 or negative as they are invalid transactions
df = df[df['sales'] > 0]
df = df[df['quantity'] > 0]

# 7. Save the Cleaned Dataset
output_path = 'data/cleaned/superstore_cleaned.csv'
df.to_csv(output_path, index=False)

# 8. Data Quality Summary
final_rows = df.shape[0]
print("\n--- DATA QUALITY SUMMARY ---")
print(f"Initial Rows: {initial_rows}")
print(f"Duplicates Removed: {duplicates_count}")
print(f"Missing Values Handled:\n{missing_values[missing_values > 0]}")
print(f"Invalid Sales/Quantity Dropped: {invalid_sales + invalid_quantity}")
print(f"Final Cleaned Rows: {final_rows}")
print(f"Cleaned dataset saved successfully to: {output_path}")