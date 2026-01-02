# Blind LLM Data Cleaning Practice

This repository demonstrates a privacy-first workflow for using Large Language Models (LLMs) to write data cleaning scripts **without ever exposing the actual data to the model.**

## The Concept

Enterprises often block LLMs due to data privacy concerns. This workflow proves that you can leverage an LLM's coding capabilities by sharing only **metadata** and **structural patterns**, keeping the raw records strictly local.

## Workflow

1.  **`00_generate_mock_data.py`**: Creates a "messy" dataset with mixed date formats, inconsistent strings, and dirty numerical fields. (Simulates your private data).
2.  **`01_analyze_schema.py`**: Runs locally to generate a **metadata-only report** (column names, types, null counts). This report is safe to share with an LLM.
3.  **`02_analyze_patterns.py`**: When simple parsing fails (e.g., dates), this script extracts **format patterns** (e.g., `DD/DD/DDDD` vs `DDDD-DD-DD`) without revealing specific values.
4.  **`03_clean_data.py`**: The LLM-generated script that uses the discovered patterns to robustly clean the data locally.

## Usage

1. **Setup**:
   ```bash
   pip install pandas
   python 00_generate_mock_data.py
   ```

2. **Analyze (The "Blind" Step)**:
   ```bash
   python 01_analyze_schema.py
   # Output serves as the prompt for the LLM
   ```

3. **Refine (Pattern Detection)**:
   ```bash
   python 02_analyze_patterns.py
   # specific analysis for tricky columns like Dates
   ```

4. **Clean**:
   ```bash
   python 03_clean_data.py
   ```

## Key Techniques Used
*   **Immutable Operations**: Original data is never overwritten.
*   **Cascading Date Parsers**: Intelligent fallback logic for mixed date formats (ISO, US, UK).
*   **Regex Extraction**: Safely pulling numeric data from mixed string fields (`70kg` -> `70.0`).
*   **Metadata-Only Prompting**: The LLM operates solely on schema definitions and error rates.
