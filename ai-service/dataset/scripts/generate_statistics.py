import pandas as pd

def generate_stats(df):
    """
    Calculates and prints dataset statistics.
    Returns the distribution dictionary for reporting.
    """
    print("\n[Statistics] Generating dataset statistics...")
    
    # Categories distribution
    cats = {
        "Software Engineer": 0, "Frontend": 0, "Backend": 0, "Full Stack": 0,
        "AI/ML": 0, "Data Science/Analyst": 0, "DevOps/Cloud": 0, "Cybersecurity": 0,
        "Mobile": 0, "QA/Testing": 0, "UI/UX": 0
    }
    for title in df["title"].astype(str).str.lower():
        if "full stack" in title or "fullstack" in title:
            cats["Full Stack"] += 1
        elif "frontend" in title or "front end" in title:
            cats["Frontend"] += 1
        elif "backend" in title or "back end" in title:
            cats["Backend"] += 1
        elif "machine learning" in title or "ml" in title or "ai" in title or "artificial" in title:
            cats["AI/ML"] += 1
        elif "data scientist" in title or "data science" in title:
            cats["Data Science/Analyst"] += 1
        elif "data analyst" in title or "analytics" in title:
            cats["Data Science/Analyst"] += 1
        elif "devops" in title or "site reliability" in title:
            cats["DevOps/Cloud"] += 1
        elif "cloud" in title or "aws" in title or "azure" in title:
            cats["DevOps/Cloud"] += 1
        elif "cyber" in title or "security" in title:
            cats["Cybersecurity"] += 1
        elif "mobile" in title or "ios" in title or "android" in title:
            cats["Mobile"] += 1
        elif "qa" in title or "test" in title or "quality assurance" in title:
            cats["QA/Testing"] += 1
        elif "ui" in title or "ux" in title or "design" in title:
            cats["UI/UX"] += 1
        else:
            cats["Software Engineer"] += 1
            
    print("\nJob Category Distribution:")
    for cat, count in cats.items():
        print(f"  {cat}: {count}")
        
    print("\nTop 10 Companies in Dataset:")
    top_companies = df["company_name"].value_counts().head(10)
    print(top_companies)
    
    return {
        "total_records": len(df),
        "categories": cats,
        "top_companies": top_companies.to_dict()
    }

if __name__ == "__main__":
    # If run standalone, test on the processed csv
    import os
    processed_dir = r"d:\PROJECTS\Internship-recommendation-engine\ai-service\dataset\processed"
    file_path = os.path.join(processed_dir, "internships_filtered.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        generate_stats(df)
    else:
        print("No processed dataset found to analyze.")
