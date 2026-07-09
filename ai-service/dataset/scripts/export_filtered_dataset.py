import os
import pandas as pd

def export(df, out_dir):
    """
    Maps columns to target schema, caps at 2000 records, and saves to CSV.
    """
    print("\n[Export] Exporting filtered dataset...")
    
    # 1. Map to target pipeline columns
    final_df = pd.DataFrame({
        "title": df["job_title"],
        "company_name": df["company"],
        "description": df["cleaned_summary"],
        "location": df["job_location"].fillna("Remote"),
        "work_type": df["job_type"].fillna("Remote"),
        "skills": df["limited_skills"],
        "apply_url": df["job_link"]
    })
    
    # 2. Limit to target range 1000 - 3000
    if len(final_df) > 2000:
        final_df = final_df.head(2000) # Keep exactly 2000 for high quality
        print("Capped dataset to 2000 high-quality records.")
        
    # 3. Write to file
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "internships_filtered.csv")
    final_df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Successfully generated {out_path} with {len(final_df)} records.")
    
    return final_df

if __name__ == "__main__":
    print("This script is meant to be imported and used by preprocess_dataset.py")
