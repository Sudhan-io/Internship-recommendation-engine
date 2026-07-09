# Dataset Engineering Module

This module is responsible for fetching, cleaning, preprocessing, validating, and generating insights for the internship dataset used by the recommendation engine.

## Directory Structure
- **`original/`**: Contains the raw, unmodified datasets (e.g., from Kaggle/LinkedIn).
- **`processed/`**: Contains the filtered, deduplicated, and schematized CSV files ready for database ingestion.
- **`scripts/`**: Core utilities supporting the preprocessing lifecycle.

## Scripts Overview
We enforce a single-responsibility architecture to maintain data integrity and avoid duplication. 

1. `preprocess_dataset.py` (Main Orchestrator)
   - Reads the raw CSV files from `original/`
   - Merges multiple dataframes (postings, skills, summaries)
   - Filters out non-technical roles, senior roles, and incomplete data
   - Cleans HTML tags and truncates excessive skills
   - Calls the other scripts below to execute the full pipeline.

2. `export_filtered_dataset.py`
   - Maps the preprocessed dataframe to the exact schema expected by the `internships` database table.
   - Caps the dataset (e.g. at 2000 records) to ensure highest quality.
   - Exports the final `.csv` to the `processed/` directory.

3. `validate_dataset.py`
   - Checks the final exported dataframe for database constraints.
   - Ensures no null values in required fields (title, company, description).
   - Validates that strings do not exceed VARCHAR(255) lengths.

4. `generate_statistics.py`
   - Generates distribution metrics on the final dataset.
   - Calculates breakdown by Tech category (Software, Data, Cloud, etc.) and top hiring companies.

## Usage
To run the full preprocessing pipeline on the `original` dataset, execute:
```bash
cd scripts/
python preprocess_dataset.py
```
This will automatically generate a new `processed/internships_filtered.csv`.
