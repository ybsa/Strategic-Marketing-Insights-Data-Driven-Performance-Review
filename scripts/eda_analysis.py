import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set output directory for plots
output_dir = r"C:\Users\wind xebec\Data_cleaning\eda_outputs"
os.makedirs(output_dir, exist_ok=True)

# Load Data
file_path = r"C:\Users\wind xebec\Data_cleaning\marketing_campaign_data_cleaned.csv"
print(f"Loading cleaned data from {file_path}...")
data = pd.read_csv(file_path, parse_dates=['start_date', 'end_date'])

# 1. Basic Stats
print("\n--- Basic Information ---")
print(data.info())
print("\n--- Descriptive Statistics ---")
print(data.describe())

# 2. Visualizations

# Set plot style
sns.set_style("whitegrid")

# Plot 1: Total Spend by Channel
plt.figure(figsize=(10, 6))
spend_by_channel = data.groupby('channel')['spend'].sum().sort_values(ascending=False)
sns.barplot(x=spend_by_channel.index, y=spend_by_channel.values, palette='viridis')
plt.title('Total Spend by Marketing Channel')
plt.xlabel('Channel')
plt.ylabel('Total Spend ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'total_spend_by_channel.png'))
print(f"Saved plot: total_spend_by_channel.png")
plt.close()

# Plot 2: Cost per Conversion (Campaign Efficiency)
effective_campaigns = data[data['conversions'] > 0].copy()
effective_campaigns['cpc'] = effective_campaigns['spend'] / effective_campaigns['conversions']

plt.figure(figsize=(10, 6))
sns.boxplot(x='channel', y='cpc', data=effective_campaigns, palette='Set2')
plt.title('Cost per Conversion Distribution by Channel')
plt.xlabel('Channel')
plt.ylabel('Cost per Conversion ($)')
upper_limit = effective_campaigns['cpc'].quantile(0.95)
plt.ylim(0, upper_limit) 
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'cost_per_conversion_by_channel.png'))
print(f"Saved plot: cost_per_conversion_by_channel.png")
plt.close()

# Plot 3: Monthly Trends
data['month'] = data['start_date'].dt.to_period('M')
monthly_metrics = data.groupby('month')[['spend', 'conversions']].sum()

fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Month')
ax1.set_ylabel('Total Spend ($)', color=color)
monthly_metrics['spend'].plot(kind='bar', ax=ax1, color=color, position=0, width=0.4, label='Spend')
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left')

ax2 = ax1.twinx() 
color = 'tab:orange'
ax2.set_ylabel('Total Conversions', color=color)
monthly_metrics['conversions'].plot(kind='bar', ax=ax2, color=color, position=1, width=0.4, label='Conversions')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper right')

plt.title('Monthly Spend vs Conversions Trend')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'monthly_trends.png'))
print(f"Saved plot: monthly_trends.png")
plt.close()

# Plot 4: Active vs Inactive Count
plt.figure(figsize=(6, 6))
active_counts = data['active'].value_counts()
plt.pie(active_counts, labels=active_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
plt.title('Active vs Inactive Campaigns')
plt.axis('equal') 
plt.savefig(os.path.join(output_dir, 'active_campaigns_pie.png'))
print(f"Saved plot: active_campaigns_pie.png")
plt.close()

print("\nEDA Completed. Visualizations saved to:", output_dir)
