import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn defaults
sns.set_theme()
sns.set_palette("husl")

# Read and prepare the data
def prepare_data():
    # Read CSV
    df = pd.read_csv('results.csv')
    
    # Print available columns to debug
    print("Available columns:", df.columns.tolist())
    
    # Calculate average metrics per instance
    df_avg = df.groupby('instance').agg({
        'best_cost': 'mean',
        'total_iterations': 'mean',
        'total_time': 'mean',
        'path_relink_time': 'mean',
        'num_improvements_elite': 'mean',
        'num_improvements_best': 'mean'
    }).reset_index()
    
    return df, df_avg

def plot_performance_metrics(df_avg):
    # Create figure with multiple subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('BRKGA Performance Analysis', fontsize=16, y=0.95)
    
    # Plot 1: Best Cost vs Solution Time
    sns.scatterplot(data=df_avg, x='best_cost', y='total_time', ax=ax1, alpha=0.6)
    ax1.set_xlabel('Best Cost Found')
    ax1.set_ylabel('Total Time (s)')
    ax1.set_title('Solution Quality vs Time')
    
    # Plot 2: Iterations vs Best Cost
    sns.scatterplot(data=df_avg, x='total_iterations', y='best_cost', ax=ax2, alpha=0.6)
    ax2.set_xlabel('Total Iterations')
    ax2.set_ylabel('Best Cost Found')
    ax2.set_title('Convergence vs Solution Quality')
    
    # Plot 3: Best Cost Distribution
    sns.boxplot(data=df_avg, y='best_cost', ax=ax3)
    ax3.set_title('Distribution of Best Costs')
    ax3.set_ylabel('Best Cost')
    
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

def plot_convergence_analysis(df_avg):
    # Create convergence analysis plot
    plt.figure(figsize=(12, 6))
    
    # Sort instances by best cost for visualization
    df_sorted = df_avg.sort_values('best_cost')
    
    # Plot iterations vs best cost
    sns.scatterplot(data=df_sorted, x='best_cost', y='total_iterations', alpha=0.6)
    
    # Add trend line
    z = np.polyfit(df_sorted['best_cost'], df_sorted['total_iterations'], 1)
    p = np.poly1d(z)
    plt.plot(df_sorted['best_cost'], p(df_sorted['best_cost']), 
             "r--", alpha=0.8, label='Trend')
    
    plt.xlabel('Best Cost Found')
    plt.ylabel('Number of Iterations')
    plt.title('Convergence Analysis by Solution Quality')
    plt.legend()
    plt.tight_layout()
    plt.savefig('brkga_convergence_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_instance_comparison(df):
    # Select top 6 instances by total time
    top_instances = df.groupby('instance')['total_time'].mean().nlargest(6).index
    
    df_subset = df[df['instance'].isin(top_instances)]
    
    # Create comparison plot
    plt.figure(figsize=(12, 6))
    
    sns.boxplot(x='instance', y='total_time', data=df_subset)
    plt.xticks(rotation=45)
    plt.xlabel('Instance')
    plt.ylabel('Total Time (s)')
    plt.title('Solution Time Comparison Across Most Time-Consuming Instances')
    
    plt.tight_layout()
    plt.savefig('brkga_instance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Prepare data
    df, df_avg = prepare_data()
    
    # Generate plots
    plot_performance_metrics(df_avg)
    plot_convergence_analysis(df_avg)
    plot_instance_comparison(df)
    
    # Print summary statistics
    print("\nBRKGA Performance Summary")
    print("-" * 50)
    print(f"Number of instances analyzed: {len(df_avg)}")
    print(f"Average solution time: {df_avg['total_time'].mean():.2f}s")
    print(f"Average number of iterations: {df_avg['total_iterations'].mean():.2f}")
    print(f"Best improvement rate: {df_avg['num_improvements_best'].mean():.2f}")
    
    # Print performance by instance
    print("\nTop 5 Most Time-Consuming Instances:")
    print(df_avg.nlargest(5, 'total_time')[['instance', 'total_time', 'best_cost']])

if __name__ == "__main__":
    main()