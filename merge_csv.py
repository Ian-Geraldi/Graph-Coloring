import pandas as pd

# Read both CSVs
df_results = pd.read_csv('results.csv')
df_opt = pd.read_csv('results - OPT.csv')

# Clean up instance names 
df_results['clean_name'] = df_results['instance'].str.replace('.col', '')
df_opt['clean_name'] = df_opt['name'].str.replace('.col', '').str.replace('.b', '')

# Print unique names from both dataframes to debug
print("Names in results.csv:")
print(sorted(df_results['clean_name'].unique()))
print("\nNames in results - OPT.csv:")
print(sorted(df_opt['clean_name'].unique()))

# Merge the dataframes
df = pd.merge(
    df_results, 
    df_opt[['clean_name', 'edges', 'opt', 'src']], 
    on='clean_name', 
    how='left'
)

# Drop the temporary column and reorder
df = df.drop('clean_name', axis=1)

# Define the desired column order
columns = [
    'instance', 'seed', 'population_size', 'elite_percentage', 
    'mutants_percentage', 'num_independent_populations', 'edges',
    'best_cost', 'opt', 'src', 'total_iterations', 'last_update_iteration',
    'total_time', 'last_update_time', 'path_relink_time',
    'path_relink_calls', 'num_improvements_elite', 'num_improvements_best'
]

# Reorder columns
df = df[columns]

# Print merge results
print("\nRows with missing data:")
print(df[df['opt'].isna()]['instance'].unique())

# Save to new CSV
df.to_csv('results_merged.csv', index=False)

print("\nCreated results_merged.csv with the following columns:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())