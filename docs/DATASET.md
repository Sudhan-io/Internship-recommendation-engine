# Dataset Engineering

The Dataset Engineering module is responsible for fetching, cleaning, preprocessing, validating, and generating insights for the baseline internship dataset. 

A high-quality dataset is crucial for the recommendation engine to provide accurate semantic matches.

## Core Module Location
The canonical dataset engineering utilities are located in:
**[`ai-service/dataset/`](../ai-service/dataset/)**

Please refer to the `README.md` inside that directory for highly specific technical execution instructions.

## Pipeline Overview
The AI recommendation engine leverages a synthesized dataset constructed from public sources (e.g. LinkedIn job postings).

1. **Original Data (`ai-service/dataset/original/`)**: Contains the raw CSV dumps. These files are treated as immutable.
2. **Preprocessing (`scripts/preprocess_dataset.py`)**: 
   - Merges multiple relational datasets (postings, skills, summaries).
   - Filters out non-technical roles, senior roles, and incomplete data.
   - Scrubs HTML markup and invalid characters.
3. **Validation (`scripts/validate_dataset.py`)**: Ensures strict compliance with the MySQL schema constraints (e.g. `VARCHAR(255)` length limits).
4. **Export (`scripts/export_filtered_dataset.py`)**: Outputs the finalized `.csv`.
5. **Processed Data (`ai-service/dataset/processed/`)**: The finalized `internships_filtered.csv` that is seeded into the MySQL database during setup.

## Current Dataset Statistics
The repository comes pre-loaded with approximately **1,000 high-quality technical internships**, spanning roles in Software Engineering, Data Science, AI/ML, DevOps, and Cybersecurity.

For a detailed breakdown of the current data distributions, run the statistics generator:
```bash
cd ai-service/dataset/scripts
python generate_statistics.py
```
