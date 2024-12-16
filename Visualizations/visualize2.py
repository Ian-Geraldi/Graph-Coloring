import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn defaults
sns.set_theme()
sns.set_palette("husl")

def prepare_data():
    # Read both CSVs
    df_results = pd.read_csv('results.csv')
    df_opt = pd.read_csv('results - OPT.csv')
    
    # Clean up instance names to match between files
    df_results['instance'] = df_results['instance'].str.replace('.col', '')
    df_opt['name'] = df_opt['name'].str.replace('.col', '')
    df_opt['name'] = df_opt['name'].str.replace('.b', '')
    
    # Merge the dataframes
    df = pd.merge(df_results, df_opt, 
                 left_on='instance', 
                 right_on='name', 
                 how='left')
    
    # Calculate gap to optimal
    df['gap_to_opt'] = ((df['best_cost'] - df['opt']) / df['opt']) * 100
    
    # Calculate density
    df['density'] = df['edges'] / (df['nodes'] * (df['nodes'] - 1) / 2)
    
    # Calculate average metrics per instance
    df_avg = df.groupby('instance').agg({
        'best_cost': 'mean',
        'opt': 'first',
        'nodes': 'first',
        'edges': 'first',
        'src': 'first',
        'total_iterations': 'mean',
        'total_time': 'mean',
        'path_relink_time': 'mean',
        'gap_to_opt': 'mean',
        'density': 'first',
        'num_improvements_elite': 'mean',
        'num_improvements_best': 'mean'
    }).reset_index()
    
    return df, df_avg

def plot_performance_metrics(df_avg):
    # Create figure with multiple subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('BRKGA Performance Analysis', fontsize=16, y=0.95)
    
    # Plot 1: Instance Size vs Gap to Optimal
    sns.scatterplot(data=df_avg, x='nodes', y='gap_to_opt', ax=ax1, alpha=0.6)
    ax1.set_xlabel('Number of Nodes')
    ax1.set_ylabel('Gap to Optimal Solution (%)')
    ax1.set_title('Instance Size vs Solution Quality')
    
    # Plot 2: Density vs Solution Time
    sns.scatterplot(data=df_avg, x='density', y='total_time', ax=ax2, alpha=0.6)
    ax2.set_xlabel('Graph Density')
    ax2.set_ylabel('Total Time (s)')
    ax2.set_title('Graph Density vs Solution Time')
    
    # Plot 3: Gap Distribution by Source
    sns.boxplot(data=df_avg, x='src', y='gap_to_opt', ax=ax3)
    ax3.set_title('Solution Quality by Instance Source')
    ax3.set_ylabel('Gap to Optimal Solution (%)')
    ax3.set_xlabel('Instance Source')
    plt.xticks(rotation=45)
    
    # Plot 4: Time Components
    time_components = df_avg[['total_time', 'path_relink_time']].mean()
    colors = ['#2ecc71', '#e74c3c']
    ax4.bar(range(len(time_components)), time_components, color=colors)
    ax4.set_xticks(range(len(time_components)))
    ax4.set_xticklabels(['Total Time', 'Path Relink Time'], rotation=45)
    ax4.set_title('Average Time Components')
    ax4.set_ylabel('Time (s)')

    plt.tight_layout()
    plt.savefig('brkga_performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_solution_quality(df_avg):
    plt.figure(figsize=(12, 6))
    
    # Sort by gap to optimal
    df_sorted = df_avg.sort_values('gap_to_opt', ascending=False)
    df_top = df_sorted.head(15)  # Top 15 instances with largest gap
    
    # Create bar plot
    sns.barplot(data=df_top, x='instance', y='gap_to_opt')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Instance')
    plt.ylabel('Gap to Optimal Solution (%)')
    plt.title('Top 15 Instances with Largest Optimality Gap')
    
    plt.tight_layout()
    plt.savefig('brkga_solution_quality.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_instance_comparison(df):
    # Select instances from different sources
    selected_instances = df.groupby('src').apply(
        lambda x: x.nlargest(2, 'total_time')['instance'].tolist()
    ).sum()
    
    df_subset = df[df['instance'].isin(selected_instances)]
    
    # Create comparison plot
    plt.figure(figsize=(12, 6))
    
    sns.boxplot(x='instance', y='total_time', data=df_subset)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Instance')
    plt.ylabel('Total Time (s)')
    plt.title('Solution Time Comparison Across Different Instance Types')
    
    plt.tight_layout()
    plt.savefig('brkga_instance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Prepare data
    df, df_avg = prepare_data()
    
    # Generate plots
    plot_performance_metrics(df_avg)
    plot_solution_quality(df_avg)
    plot_instance_comparison(df)
    
    # Print summary statistics
    print("\nBRKGA Performance Summary")
    print("-" * 50)
    print(f"Number of instances analyzed: {len(df_avg)}")
    print(f"Average solution time: {df_avg['total_time'].mean():.2f}s")
    print(f"Average gap to optimal: {df_avg['gap_to_opt'].mean():.2f}%")
    print(f"Number of instances solved to optimality: {len(df_avg[df_avg['gap_to_opt'] == 0])}")
    
    # Print performance by instance source
    print("\nPerformance by Instance Source:")
    source_stats = df_avg.groupby('src').agg({
        'gap_to_opt': ['mean', 'std'],
        'total_time': 'mean',
        'instance': 'count'
    }).round(2)
    print(source_stats)
    
    # Print worst performing instances
    print("\nTop 5 Instances with Largest Optimality Gap:")
    print(df_avg.nlargest(5, 'gap_to_opt')[['instance', 'gap_to_opt', 'total_time', 'src']])

if __name__ == "__main__":
    main()