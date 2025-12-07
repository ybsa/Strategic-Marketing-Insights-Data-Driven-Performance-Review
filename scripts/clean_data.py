import pandas as pd
import numpy as np
import re

def clean_currency(x):
    if isinstance(x, str):
        # Remove '$', ',', and whitespace
        x = re.sub(r'[$,\s]', '', x)
        try:
            return float(x)
        except ValueError:
            return np.nan
    return x

def clean_active(x):
    if pd.isna(x):
        return False # Assuming False if missing for now, or could use None
    x_str = str(x).lower().strip()
    if x_str in ['y', 'yes', 'true', '1', '1.0']:
        return True
    elif x_str in ['n', 'no', 'false', '0', '0.0']:
        return False
    return False # Default fallback

# Load Data
file_path = r"C:\Users\wind xebec\Data_cleaning\marketing_campaign_data_messy.csv"
print(f"Loading data from {file_path}...")
df = pd.read_csv(file_path)

# Standardize Columns
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print(f"Columns: {df.columns.tolist()}")

# Handle Duplicate Columns
# Pandas might have duplicate column names if they were exactly the same in CSV, but read_csv typically mangles them active.
# However, if we normalized names, we might have created duplicates (e.g., 'Clicks' and 'Clicks ').
print(f"Columns after normalization: {df.columns.tolist()}")

# Remove duplicate columns by keeping the first occurrence
# If appropriate, we could check which one has more data, but usually the first one is correct.
# Let's count non-nulls for duplicates to be sure.
counts = {}
for col in df.columns:
    counts[col] = counts.get(col, 0) + 1

duplicates = [col for col, count in counts.items() if count > 1]
if duplicates:
    print(f"Found duplicate columns: {duplicates}")
    for dup in duplicates:
        # Get all locations
        locs = np.where(df.columns == dup)[0]
        # Calculate non-nulls for each instance
        valid_counts = [df.iloc[:, i].count() for i in locs]
        best_idx = locs[np.argmax(valid_counts)] # Keep the one with most data
        
        print(f"Resolving duplicate '{dup}': Keeping index {best_idx} with {max(valid_counts)} non-nulls.")
        
        # Create a list of columns to keep
        cols_to_keep = [i for i in range(df.shape[1]) if i == best_idx or df.columns[i] != dup]
        df = df.iloc[:, cols_to_keep]

print(f"Columns after deduplication: {df.columns.tolist()}")

# Date Cleaning
print("Cleaning dates...")
# Convert to datetime, coercing errors to NaT initially
df['start_date'] = pd.to_datetime(df['start_date'], dayfirst=True, errors='coerce')
df['end_date'] = pd.to_datetime(df['end_date'], dayfirst=True, errors='coerce') 

# Channel Cleaning
print("Cleaning channels...")
channel_map = {
    'facebok': 'Facebook',
    'facebook': 'Facebook',
    'gogle': 'Google Ads',
    'google ads': 'Google Ads',
    'tik_tok': 'TikTok',
    'tiktok': 'TikTok',
    'e-mail': 'Email',
    'email': 'Email',
    'instagram': 'Instagram',
    'insta_gram': 'Instagram'
}
def normalize_channel(x):
    if pd.isna(x): return 'Unknown'
    x = str(x).strip().lower()
    if x in ['n/a', 'xx', 'invalid', 'nan']: return 'Unknown'
    return channel_map.get(x, x.title())

df['channel'] = df['channel'].apply(normalize_channel)

# Active Cleaning
print("Cleaning active flag...")
df['active'] = df['active'].apply(clean_active)

# Numerical Cleaning
print("Cleaning numerical columns...")
df['spend'] = df['spend'].apply(clean_currency)
# Impressions, Clicks, Conversions -> coerce to numeric
numeric_cols = ['impressions', 'clicks', 'conversions']
for col in numeric_cols:
    if col in df.columns:
        # Ensure we operate on a Series, not DataFrame (should be guaranteed by dedupe above)
        print(f"Processing column: {col}")
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Missing Values Logic (Simple Imputation/Dropping)
# For this pass, we will just fill missing 'conversions' with 0 if 'clicks' > 0, else 0
if 'conversions' in df.columns:
    df['conversions'] = df['conversions'].fillna(0)

# Save Cleaned Data
output_path = r"C:\Users\wind xebec\Data_cleaning\marketing_campaign_data_cleaned.csv"
df.to_csv(output_path, index=False)
print(f"Cleaned data saved to {output_path}")

# Verification Stats
print("\n--- Verification Stats ---")
print(f"Shape: {df.shape}")
print(f"Missing Values:\n{df.isnull().sum()}")
if 'channel' in df.columns:
    print(f"\nUnique Channels: {df['channel'].unique()}")
if 'active' in df.columns:
    print(f"Active Counts:\n{df['active'].value_counts()}")
