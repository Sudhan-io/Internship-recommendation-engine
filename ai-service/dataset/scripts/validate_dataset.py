import pandas as pd

def validate(df):
    """
    Validates dataset constraints:
    - No nulls in required fields
    - String length limits (e.g., skills < 255)
    """
    print("\n[Validation] Running dataset constraints validation...")
    issues = []
    
    # 1. Null checks
    required_cols = ["title", "company_name", "description", "skills"]
    for col in required_cols:
        if df[col].isnull().any():
            issues.append(f"Column '{col}' contains null values.")
            
    # 2. String length checks (Database VARCHAR limits)
    max_lengths = {
        "title": 255,
        "company_name": 255,
        "skills": 255
    }
    
    for col, max_len in max_lengths.items():
        # Using string length
        over_length = df[col].astype(str).str.len() > max_len
        if over_length.any():
            count = over_length.sum()
            issues.append(f"Column '{col}' has {count} rows exceeding {max_len} characters.")
            
    if issues:
        print("[Validation] FAILED:")
        for issue in issues:
            print(f" - {issue}")
        return False
    
    print("[Validation] PASSED: All constraints met.")
    return True

if __name__ == "__main__":
    # If run standalone, test on the processed csv
    import os
    processed_dir = r"d:\PROJECTS\Internship-recommendation-engine\ai-service\dataset\processed"
    file_path = os.path.join(processed_dir, "internships_filtered.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        validate(df)
    else:
        print("No processed dataset found to validate.")
