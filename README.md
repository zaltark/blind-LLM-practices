# Blind LLM Data Cleaning Practice

A privacy-first workflow for using Large Language Models (LLMs) to clean data without ever exposing raw records to the model.

## Core Methodology
This project demonstrates how to provide an LLM with **structural metadata** and **pattern analysis** instead of raw data. The LLM then generates cleaning logic that is executed locally.

## File Reference

### 00_generate_mock_data.py
*   **Purpose**: Creates a reproducible messy dataset for testing.
*   **Outputs**: `Test1/raw_extract.csv`.
*   **Data Features**: Mixed date formats (ISO, Day-First, US-Slash), numerical fields with string suffixes ("kg", "lbs"), and inconsistent categorical strings.

### 01_analyze_schema.py
*   **Purpose**: Extracts the non-sensitive structure of the data.
*   **Outputs**: Console table showing Column Names, Dtypes, Null Counts, and Unique Value counts.
*   **Privacy**: Does not print or store actual row values.

### 02_analyze_patterns.py
*   **Purpose**: Deep-dives into parsing failures.
*   **Outputs**: A frequency distribution of character patterns (e.g., `DDDD-DD-DD` vs `DD/DD/DDDD`).
*   **Privacy**: Transmutes specific data points into generic structural tokens (D=Digit, A=Alpha).

### 03_clean_data.py
*   **Purpose**: Executes the LLM-derived cleaning strategy.
*   **Logic**: 
    - Standardizes gender to single-character codes.
    - Uses Regex to extract floats from mixed-string weight fields.
    - Implements a cascading date parser to resolve multiple conflicting formats into standard `datetime` objects.
*   **Outputs**: `cleaned_data.csv` (schema: `patient_id`, `dob`, `gender`, `height_cm`, `notes`, `weight_kg`).

## Workflow Summary
1.  **Generate** dummy data locally.
2.  **Analyze** the schema to get column names and types.
3.  **Pattern Analyze** failing columns to identify specific formatting variations.
4.  **Clean** using the generated script that targets the identified patterns.