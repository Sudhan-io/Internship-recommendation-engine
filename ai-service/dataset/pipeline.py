import os
import re
import csv
import mysql.connector
from typing import Dict, List, Tuple, Any

from normalization.canonical_dictionary import CanonicalDictionary
from normalization.skill_normalizer import SkillNormalizer
from normalization.company_normalizer import CompanyNormalizer

class IngestionPipeline:
    def __init__(self, db_config: dict = None):
        self.canonical_dict = CanonicalDictionary()
        self.skill_normalizer = SkillNormalizer(self.canonical_dict)
        self.company_normalizer = CompanyNormalizer(self.canonical_dict)
        self.db_config = db_config if db_config is not None else self._load_db_config()

    def _load_db_config(self) -> dict:
        config = {
            "host": "localhost",
            "user": "root",
            "password": "Password",
            "database": "internship_recommendation_engine"
        }
        
        # Load .env file manually if it exists
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            env_path = os.path.join(current_dir, ".env")
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ[k.strip()] = v.strip()
        except Exception as e:
            print(f"Warning: Failed to load .env file: {e}")

        # Read environment variables directly with fallbacks
        db_url = os.environ.get("DB_URL", "jdbc:mysql://localhost:3306/internship_recommendation_engine")
        db_user = os.environ.get("DB_USERNAME", "root")
        db_pass = os.environ.get("DB_PASSWORD", "Sudh@007")

        # Parse DB_URL to get host and database name
        match = re.search(r"//([^:/]+):?(\d*)/([^?/\s]+)", db_url)
        if match:
            config["host"] = match.group(1)
            config["database"] = match.group(3)

        config["user"] = db_user
        config["password"] = db_pass

        return config

    def clean_html(self, text: str) -> str:
        if not text:
            return ""
        clean = re.compile(r"<[^>]+>")
        text = clean.sub("", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def normalize_mode(self, work_type: str) -> str:
        wt = str(work_type).lower().strip()
        if any(kw in wt for kw in ["remote", "online", "virtual", "wfh"]):
            return "ONLINE"
        elif any(kw in wt for kw in ["hybrid", "mixed", "flexible"]):
            return "HYBRID"
        elif any(kw in wt for kw in ["onsite", "on-site", "office", "offline", "in-person"]):
            return "OFFLINE"
        return "OFFLINE"

    def clean_row(self, row: dict) -> Dict[str, Any]:
        title = row.get("title", "").strip()
        company = row.get("company_name", "").strip()
        description = row.get("description", "").strip()
        
        if not title or not company or not description:
            raise ValueError("Missing required fields (title, company_name, description)")
            
        clean_desc = self.clean_html(description)
        
        norm_company_list, _ = self.company_normalizer.normalize([company])
        norm_company = norm_company_list[0] if norm_company_list else company
        
        location = row.get("location", "").strip()
        if not location:
            location = "Remote" if self.normalize_mode(row.get("work_type", "")) == "ONLINE" else "Unspecified"
            
        mode = self.normalize_mode(row.get("work_type", ""))
        
        skills_str = row.get("skills", "")
        raw_skills = [s.strip() for s in re.split(r",|;|/|\s+and\s+", skills_str) if s.strip()]
        norm_skills, _ = self.skill_normalizer.normalize(raw_skills)
        
        return {
            "title": title,
            "company_name": norm_company,
            "description": clean_desc,
            "location": location,
            "mode": mode,
            "skills": norm_skills,
            "apply_url": row.get("apply_url", "").strip()
        }

    def import_csv(self, csv_filepath: str) -> Tuple[int, int]:
        if not os.path.exists(csv_filepath):
            raise FileNotFoundError(f"CSV file not found: {csv_filepath}")
            
        cleaned_records = []
        rejected_count = 0
        seen_duplicates = set()
        
        with open(csv_filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    cleaned = self.clean_row(row)
                    dup_key = (cleaned["title"].lower(), cleaned["company_name"].lower())
                    if dup_key in seen_duplicates:
                        continue
                    seen_duplicates.add(dup_key)
                    cleaned_records.append(cleaned)
                except Exception as e:
                    print(f"Skipping row due to validation failure: {e}")
                    rejected_count += 1
                    
        imported_count = self._load_to_database(cleaned_records)
        return imported_count, rejected_count

    def _load_to_database(self, records: List[Dict[str, Any]]) -> int:
        conn = None
        cursor = None
        imported_count = 0
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            for rec in records:
                cursor.execute(
                    "SELECT internship_id FROM internships WHERE LOWER(title) = %s AND LOWER(company) = %s",
                    (rec["title"].lower(), rec["company_name"].lower())
                )
                res = cursor.fetchone()
                if res:
                    internship_id = res[0]
                else:
                    skills_joined = ", ".join(rec["skills"])
                    cursor.execute(
                        """INSERT INTO internships 
                           (title, company, location, mode, description, apply_url, required_skills) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (rec["title"], rec["company_name"], rec["location"], rec["mode"], rec["description"], rec["apply_url"], skills_joined)
                    )
                    internship_id = cursor.lastrowid
                    imported_count += 1
                    
                for skill_name in rec["skills"]:
                    cursor.execute("SELECT skill_id FROM skills WHERE LOWER(skill_name) = %s", (skill_name.lower(),))
                    s_res = cursor.fetchone()
                    if s_res:
                        skill_id = s_res[0]
                    else:
                        cursor.execute("INSERT INTO skills (skill_name) VALUES (%s)", (skill_name,))
                        skill_id = cursor.lastrowid
                        
                    cursor.execute(
                        "SELECT internship_skill_id FROM internship_skills WHERE internship_id = %s AND skill_id = %s",
                        (internship_id, skill_id)
                    )
                    link_res = cursor.fetchone()
                    if not link_res:
                        cursor.execute(
                            "INSERT INTO internship_skills (internship_id, skill_id) VALUES (%s, %s)",
                            (internship_id, skill_id)
                        )
                        
            conn.commit()
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError(f"Database insertion failed: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
        return imported_count
