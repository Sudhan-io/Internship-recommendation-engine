import json
import os
from typing import List

class SkillsRepository:
    def __init__(self, filepath: str = None):
        if filepath is None:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = os.path.join(current_dir, "dataset", "skills.json")
        self.filepath = filepath
        self.skills = self._load_skills()

    def _load_skills(self) -> List[str]:
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading skills from {self.filepath}: {e}")
            return []

    def get_all_skills(self) -> List[str]:
        return self.skills
