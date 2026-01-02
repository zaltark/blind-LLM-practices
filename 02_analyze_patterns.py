import pandas as pd
import re
import os

def analyze_date_patterns(filepath, col_name):
    df = pd.read_csv(filepath)
    series = df[col_name].dropna()
    
    # Identify what pd.to_datetime fails on
    failed_mask = pd.to_datetime(series, errors='coerce').isna()
    failed_samples = series[failed_mask]
    
    if failed_samples.empty:
        print(f"No parsing failures detected in {col_name}")
        return

    print(f"Analyzing {len(failed_samples)} failed patterns for '{col_name}':")
    
    patterns = {}
    for val in failed_samples:
        # Create a generic pattern: '2023-01-01' -> 'DDDD-DD-DD'
        # 'Jan 01, 2023' -> 'AAA DD, DDDD'
        pattern = ""
        for char in str(val):
            if char.isdigit(): pattern += "D"
            elif char.isalpha(): pattern += "A"
            elif char.isspace(): pattern += "_"
            else: pattern += char
        
        patterns[pattern] = patterns.get(pattern, 0) + 1
    
    # Sort by frequency
    for p, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
        print(f"Pattern: {p:<20} | Count: {count}")

if __name__ == "__main__":
    analyze_date_patterns(os.path.join("Test1", "raw_extract.csv"), "dob")
