# Blind LLM Data Cleaning Practice
A privacy-first workflow for using Large Language Models (LLMs) to clean data without ever exposing raw records to the model.

## Core Methodology
Enterprises often block LLM usage due to data leakage risks. This project demonstrates a compliant workaround: **Metadata Abstraction.**

Instead of uploading raw data (CSV/SQL) to the AI, we run local scripts to generate structural metadata and tokenized pattern analysis. The LLM acts as a logic engine, receiving only these safe artifacts to generate cleaning scripts, which are then executed locally.

## 📂 File Reference

### 00_generate_mock_data.py
**Purpose**: Creates a reproducible, messy dataset for testing the pipeline.

**Data Features**:
* Mixed date formats (ISO, Day-First, US-Slash).
* Numerical fields polluted with string suffixes ("70kg", "150lbs").
* Inconsistent categorical strings ("M", "Male", "f").

**Outputs**: `Test1/raw_extract.csv`

### 01_analyze_schema.py
**Purpose**: Extracts the non-sensitive structure of the data to inform the LLM of the "shape" of the problem.

**Privacy**: Strictly Aggregate. Does not print, store, or transmit actual row values.

**Outputs**: Console table displaying:
* Column Names & Data Types
* Null Counts & Percentages
* Unique Value Counts

### 02_analyze_patterns.py
**Purpose**: Deep-dives into parsing failures (specifically for dates and mixed types) to help the LLM write robust parsers.

**Privacy**: Tokenization. Transmutes specific data points into generic structural tokens (e.g., `1990-05-20` becomes `DDDD-DD-DD` where D=Digit).

**Outputs**: A frequency distribution of character patterns, allowing the LLM to see formats without seeing dates.

### 03_clean_data.py
**Purpose**: The "Blind Surgeon." Executes the cleaning strategy derived by the LLM based on the metadata from steps 01 and 02.

**Logic Implemented**:
* **Categorical**: Standardizes gender to single-character codes via mapping.
* **Numerical**: Uses Regex to safely extract floats from mixed-string weight fields (handling unit conversion).
* **Temporal**: Implements a Cascading Date Parser to resolve conflicting formats (e.g., trying ISO first, then US, then EU) to ensure 100% data retention.

**Outputs**: `cleaned_data.csv` (Schema: `patient_id`, `dob`, `gender`, `height_cm`, `notes`, `weight_kg`).

## 🚀 Workflow Summary
1.  **Generate** dummy data locally using the chaos script.
2.  **Analyze Schema** to obtain safe column definitions and error rates.
3.  **Analyze Patterns** on failing columns to identify specific formatting variations via tokenization.
4.  **Clean** the data using the LLM-generated script that targets the identified patterns without ever touching the source file.
