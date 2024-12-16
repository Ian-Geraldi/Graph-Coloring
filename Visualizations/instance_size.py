import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Read and prepare data
df = pd.read_csv('results.csv')
df_opt = pd.read_csv('results - OPT.csv')

# Clean names and merge
df['clean_name'] = df['instance'].str.replace('.col', '')
df_opt['clean_name'] = df_opt['name'].str.replace('.col', '').str.replace('.b', '')
df = pd.merge(df, df_opt[['clean_name', 'nodes']], on='clean_name', how='left')

# Remove any rows with NaN values
df = df.dropna(subset=['nodes', 'last_update_iteration'])

# Calculate averages per instance
df_avg = df.groupby('clean_name').agg({
    'last_update_iteration': 'mean',
    'nodes': 'first'
}).reset_index()

print("\nData Overview:")
print(f"Number of instances: {len(df_avg)}")
print("\nSample of the data:")
print(df_avg.head())

# Create the main scatter plot
plt.figure(figsize=(12, 8))

# Scatter plot
sns.scatterplot(data=df_avg, x='nodes', y='last_update_iteration', alpha=0.6)

try:
    # Try to add trend line
    z = np.polyfit(df_avg['nodes'], df_avg['last_update_iteration'], 1)
    p = np.poly1d(z)
    x_range = np.linspace(df_avg['nodes'].min(), df_avg['nodes'].max(), 100)
    plt.plot(x_range, p(x_range), "r--", alpha=0.8, label=f'Linear trend')
except np.linalg.LinAlgError:
    print("Warning: Could not compute linear trend line due to numerical issues")

# Calculate correlation coefficient
correlation = stats.pearsonr(df_avg['nodes'], df_avg['last_update_iteration'])

# Add annotations
plt.title('Instance Size vs Last Update Iteration')
plt.xlabel('Number of Nodes')
plt.ylabel('Last Update Iteration')
plt.text(0.05, 0.95, f'Correlation: {correlation[0]:.3f}\np-value: {correlation[1]:.3f}', 
         transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8))

# Find outliers for labeling
Q1 = df_avg['last_update_iteration'].quantile(0.25)
Q3 = df_avg['last_update_iteration'].quantile(0.75)
IQR = Q3 - Q1
threshold = Q3 + 1.5 * IQR

# Add instance labels for outliers
outliers = df_avg[df_avg['last_update_iteration'] > threshold]
for idx, row in outliers.iterrows():
    plt.annotate(row['clean_name'], (row['nodes'], row['last_update_iteration']), 
                xytext=(5, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('last_update_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Statistical analysis
print("\nStatistical Analysis of Last Update Iteration vs Instance Size")
print("-" * 60)

# Basic statistics
print("\nBasic Statistics:")
print(df_avg[['nodes', 'last_update_iteration']].describe().round(2))

# Find instances with highest last_update_iteration
print("\nTop 10 Instances with Highest Last Update Iteration:")
print(df_avg.nlargest(10, 'last_update_iteration')[
    ['clean_name', 'nodes', 'last_update_iteration']
].round(2))

# Calculate and print correlation statistics
print("\nCorrelation Analysis:")
print(f"Pearson correlation coefficient: {correlation[0]:.3f}")
print(f"P-value: {correlation[1]:.3f}")

# Group by node ranges
node_ranges = [0, 100, 200, 500, float('inf')]
labels = ['<100 nodes', '100-200 nodes', '200-500 nodes', '>500 nodes']
df_avg['size_range'] = pd.cut(df_avg['nodes'], bins=node_ranges, labels=labels)

# Print summary by size range
print("\nSummary by Size Range:")
size_summary = df_avg.groupby('size_range').agg({
    'last_update_iteration': ['count', 'mean', 'std', 'min', 'max']
}).round(2)
print(size_summary)

# Additional analysis of extreme cases
print("\nInstances with Early Updates (First 10 iterations):")
print(df_avg[df_avg['last_update_iteration'] <= 10][
    ['clean_name', 'nodes', 'last_update_iteration']
].sort_values('last_update_iteration'))

print("\nInstances with Late Updates (>90th percentile):")
late_threshold = df_avg['last_update_iteration'].quantile(0.9)
print(df_avg[df_avg['last_update_iteration'] > late_threshold][
    ['clean_name', 'nodes', 'last_update_iteration']
].sort_values('last_update_iteration', ascending=False))