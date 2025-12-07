import pandas as pd
import numpy as np

# Load Data
file_path = r"C:\Users\wind xebec\Data_cleaning\marketing_campaign_data_cleaned.csv"
df = pd.read_csv(file_path, parse_dates=['start_date', 'end_date'])

# Feature Engineering
df['cpc'] = df['spend'] / df['clicks']
df['cpa'] = df['spend'] / df['conversions']
df['cvr'] = df['conversions'] / df['clicks']
df['roi'] = (df['conversions'] * 100 - df['spend']) / df['spend'] # Dummy revenue assumption: $100 per conversion

# Remove infinite values from division by zero
df.replace([np.inf, -np.inf], np.nan, inplace=True)

print("--- CHANNEL PERFORMANCE ---")
channel_stats = df.groupby('channel').agg({
    'spend': 'sum',
    'conversions': 'sum',
    'clicks': 'sum',
    'campaign_id': 'count'
}).reset_index()

channel_stats['cpa'] = channel_stats['spend'] / channel_stats['conversions']
channel_stats['cvr'] = channel_stats['conversions'] / channel_stats['clicks']
channel_stats = channel_stats.sort_values('cpa')

print(channel_stats)

print("\n--- CORRELATIONS ---")
corr = df[['spend', 'clicks', 'impressions', 'conversions']].corr()
print(corr)

print("\n--- CAMPAIGN DURATION VS PERFORMANCE ---")
df['duration_days'] = (df['end_date'] - df['start_date']).dt.days
duration_perf = df.groupby(pd.cut(df['duration_days'], bins=[0, 7, 14, 30, 100])).agg({
    'cpa': 'mean',
    'conversions': 'mean'
})
print(duration_perf)

print("\n--- KEY INSIGHTS GENERATION ---")
best_channel = channel_stats.iloc[0]['channel']
worst_channel = channel_stats.iloc[-1]['channel']
print(f"Most Efficient Channel (Lowest CPA): {best_channel} (${channel_stats.iloc[0]['cpa']:.2f})")
print(f"Least Efficient Channel (Highest CPA): {worst_channel} (${channel_stats.iloc[-1]['cpa']:.2f})")

avg_active_cpa = df[df['active']]['cpa'].mean()
avg_inactive_cpa = df[~df['active']]['cpa'].mean()
print(f"Active Campaigns Avg CPA: ${avg_active_cpa:.2f}")
print(f"Inactive Campaigns Avg CPA: ${avg_inactive_cpa:.2f}")
