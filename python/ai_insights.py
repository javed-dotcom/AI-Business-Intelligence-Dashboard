import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

print("Starting AI Customer Segmentation...")

# 1. Load the cleaned dataset
df = pd.read_csv('data/cleaned/superstore_cleaned.csv')

# 2. Aggregate data by Customer (Total Sales, Total Profit, and Number of Orders)
customer_data = df.groupby(['customer_id', 'customer_name']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()
customer_data.rename(columns={'order_id': 'total_orders'}, inplace=True)

# 3. Scale the features
# ML algorithms need all numbers on a similar scale so 'sales' (in thousands) 
# doesn't overpower 'total_orders' (usually 1 to 10).
scaler = StandardScaler()
features_to_scale = customer_data[['sales', 'profit', 'total_orders']]
scaled_features = scaler.fit_transform(features_to_scale)

# 4. Apply AI Model: K-Means Clustering
# We are telling the AI to find 3 distinct groups of customers
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
customer_data['cluster'] = kmeans.fit_predict(scaled_features)

# 5. Label the AI Clusters with Business Terms
# We calculate the average sales for each cluster to identify which is which
cluster_sales = customer_data.groupby('cluster')['sales'].mean().sort_values()

# Map the clusters based on spending (Lowest to Highest)
segment_labels = {
    cluster_sales.index[0]: 'Low-Value Customers',
    cluster_sales.index[1]: 'Standard Customers',
    cluster_sales.index[2]: 'High-Value VIPs'
}
customer_data['ai_segment'] = customer_data['cluster'].map(segment_labels)

# 6. Save the AI-enhanced data for Power BI
os.makedirs('data/processed', exist_ok=True)
output_path = 'data/processed/ai_customer_segments.csv'
customer_data.to_csv(output_path, index=False)

# 7. Print the results
print("\n--- AI SEGMENTATION RESULTS ---")
print(customer_data['ai_segment'].value_counts())
print(f"\nAI Customer Segments saved successfully to: {output_path}")