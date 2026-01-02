import pandas as pd
import sqlite3
import os

def print_header(title):
    print(f"\n{'='*20} {title} {'='*20}")

def analyze_dataframe(df, source_name):
    print_header(f"Analysis Report: {source_name}")
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    print("\n[Column Analysis]")
    print(f"{ 'Column':<20} | { 'Dtype':<10} | { 'Nulls':<10} | { 'Null %':<10} | { 'Unique':<10}")
    print("-" * 75)
    
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        unique_count = df[col].nunique()
        dtype = str(df[col].dtype)
        
        # Detect mixed types in object columns
        mixed_warning = ""
        if dtype == 'object':
            # Check if column contains multiple types (excluding nulls)
            types_in_col = df[col].dropna().apply(type).unique()
            if len(types_in_col) > 1:
                type_names = [t.__name__ for t in types_in_col]
                mixed_warning = f" !! MIXED TYPES: {type_names}"
        
        print(f"{col:<20} | {dtype:<10} | {null_count:<10} | {null_pct:<9.2f}% | {unique_count:<10}{mixed_warning}")

def analyze_csv(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return

    try:
        df = pd.read_csv(filepath)
        analyze_dataframe(df, f"CSV: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Error reading CSV {filepath}: {e}")

def analyze_sqlite(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return

    try:
        conn = sqlite3.connect(f"file:{filepath}?mode=ro", uri=True) # Read-only mode
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print_header(f"SQLite DB: {os.path.basename(filepath)}")
        print(f"Found {len(tables)} tables.")
        
        for table_name in tables:
            table = table_name[0]
            try:
                # Read table into dataframe for consistent analysis
                # Safe for small datasets as checked (24KB)
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                analyze_dataframe(df, f"Table: {table}")
            except Exception as e:
                print(f"Error analyzing table {table}: {e}")
                
        conn.close()
    except Exception as e:
        print(f"Error connecting to DB {filepath}: {e}")

if __name__ == "__main__":
    csv_path = os.path.join("Test1", "raw_extract.csv")
    db_path = os.path.join("Test1", "hospital_v3.db")
    
    analyze_csv(csv_path)
    analyze_sqlite(db_path)
