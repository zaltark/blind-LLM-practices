import pandas as pd
import re
import os

def clean_gender(value):
    if pd.isna(value):
        return "Unknown"
    # Standardize to first letter, uppercase (e.g., 'Male' -> 'M', 'f' -> 'F')
    s = str(value).strip().upper()
    if s.startswith('M'): return 'M'
    if s.startswith('F'): return 'F'
    if s.startswith('O'): return 'O' # Other
    return 'Unknown'

def clean_weight(value):
    if pd.isna(value):
        return None
    # Extract only the numeric part (handling cases like '70kg' or '150 lbs')
    match = re.search(r"(\d+\.?\d*)", str(value))
    if match:
        return float(match.group(1))
    return None

def robust_date_parser(series):
    """
    Attempts to parse dates using a cascading strategy based on identified patterns.
    """
    # 1. Primary Attempt: Inferred Day-First (Effective for ~50% of data)
    parsed = pd.to_datetime(series, dayfirst=True, errors='coerce')
    
    # Check what's still missing
    mask_null = parsed.isna() & series.notna()
    if not mask_null.any():
        return parsed

    print(f"  > Initial parsing left {mask_null.sum()} nulls. Applying targeted patterns...")

    # 2. Target Pattern: DDDD-DD-DD (ISO Format: YYYY-MM-DD) - Accounts for ~50 rows
    if mask_null.any():
        print("    - Attempting ISO format (YYYY-MM-DD)...")
        iso_parsed = pd.to_datetime(series[mask_null], format='%Y-%m-%d', errors='coerce')
        parsed = parsed.combine_first(iso_parsed)
        
        # Report progress
        mask_null = parsed.isna() & series.notna()
        print(f"      Remaining nulls: {mask_null.sum()}")

    # 3. Target Pattern: Slash Formats (DD/MM/YYYY or similar) - Accounts for ~24 rows
    # We try day-first slash format explicitly for the remaining items
    if mask_null.any():
        print("    - Attempting Slash format (DD/MM/YYYY)...")
        # infer_datetime_format is deprecated, but explicit format strings are fast
        slash_parsed = pd.to_datetime(series[mask_null], format='%d/%m/%Y', errors='coerce')
        parsed = parsed.combine_first(slash_parsed)
        
        mask_null = parsed.isna() & series.notna()
        print(f"      Remaining nulls: {mask_null.sum()}")

    # 4. Final Fallback: US Format (MM/DD/YYYY) just in case
    if mask_null.any():
         print("    - Attempting US Slash format (MM/DD/YYYY)...")
         us_parsed = pd.to_datetime(series[mask_null], format='%m/%d/%Y', errors='coerce')
         parsed = parsed.combine_first(us_parsed)

    return parsed

def clean_dataset(df):
    """
    Clean the dataframe using immutable-style operations.
    Returns a new cleaned dataframe.
    """
    cleaned = df.copy()
    
    # 1. Normalize Gender
    if 'gender' in cleaned.columns:
        cleaned['gender'] = cleaned['gender'].apply(clean_gender)
    
    # 2. Extract Numeric Weight
    if 'weight_raw' in cleaned.columns:
        cleaned['weight_kg'] = cleaned['weight_raw'].apply(clean_weight)
        # Drop raw column to ensure data cleanliness
        cleaned = cleaned.drop(columns=['weight_raw'])
    
    # 3. Standardize Dates (Robust)
    date_cols = ['dob', 'visit_date']
    for col in date_cols:
        if col in cleaned.columns:
            print(f"Processing Date Column: {col}")
            original_count = len(cleaned)
            cleaned[col] = robust_date_parser(cleaned[col])
            
    # 4. Enforce Types
    if 'height_cm' in cleaned.columns:
        cleaned['height_cm'] = pd.to_numeric(cleaned['height_cm'], errors='coerce')
        
    return cleaned

def process_files():
    input_csv = os.path.join("Test1", "raw_extract.csv")
    output_csv = "cleaned_data.csv"
    
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} not found.")
        return

    # Load
    df = pd.read_csv(input_csv)
    
    # Clean
    cleaned_df = clean_dataset(df)
    
    # Save (Immutable principle: original file is never overwritten)
    cleaned_df.to_csv(output_csv, index=False)
    
    # Output Metadata for Verification
    print(f"Success: Cleaned data saved to {output_csv}")
    print(f"Original shape: {df.shape}")
    print(f"Cleaned shape:  {cleaned_df.shape}")
    print("\n--- Cleaned Schema ---")
    print(cleaned_df.dtypes)
    print("\n--- Null Check in Cleaned Data ---")
    print(cleaned_df.isnull().sum())

if __name__ == "__main__":
    process_files()
