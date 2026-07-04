import json
import os
from typing import Dict, List, Set

class CanonicalDictionary:
    def __init__(self, dataset_dir: str = None):
        if dataset_dir is None:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dataset_dir = os.path.join(current_dir, "dataset")
            
        self.skills_file = os.path.join(dataset_dir, "skills.json")
        self.education_file = os.path.join(dataset_dir, "education.json")
        self.companies_file = os.path.join(dataset_dir, "companies.json")
        
        self.skills: Dict[str, str] = self._load_skills()
        self.education: Dict[str, str] = self._load_json_dict(self.education_file)
        self.companies: Dict[str, str] = self._load_json_dict(self.companies_file)

    def _load_skills(self) -> Dict[str, str]:
        # Maps lowercase skill -> canonical skill representation
        try:
            if os.path.exists(self.skills_file):
                with open(self.skills_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {skill.lower(): skill for skill in data}
            return {}
        except Exception as e:
            print(f"Error loading skills.json: {e}")
            return {}

    def _load_json_dict(self, filepath: str) -> Dict[str, str]:
        # Maps lowercase key -> canonical value
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {key.lower().strip(): val for key, val in data.items()}
            return {}
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}

    def get_canonical_skill(self, skill: str) -> str:
        # Check case-insensitively
        key = skill.lower().strip()
        # Handle some common spelling cleanups
        key = key.replace(" ", "").replace("-", "")
        for dict_key, canonical_val in self.skills.items():
            clean_dict_key = dict_key.replace(" ", "").replace("-", "")
            if key == clean_dict_key:
                return canonical_val
        return skill # fallback if not found

    def get_canonical_education(self, ed_str: str) -> str:
        key = ed_str.lower().strip()
        # Look for exact degree matches in the dictionary
        for dict_key, canonical_val in self.education.items():
            if dict_key in key:
                return canonical_val
        return ed_str # fallback if not found

    def get_canonical_company(self, company_str: str) -> str:
        key = company_str.lower().strip()
        if key in self.companies:
            return self.companies[key]
        return company_str
