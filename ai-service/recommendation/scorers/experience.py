from recommendation.scorers.base import Scorer
from typing import Dict, Any

class ExperienceScorer(Scorer):
    @property
    def weight(self) -> float:
        return 0.10

    def calculate_score(self, resume: Dict[str, Any], internship: Dict[str, Any], similarity_score: float) -> float:
        companies = resume.get("companies", {}).get("normalized", [])
        num_roles = len(companies)
        
        if num_roles >= 2:
            return 1.0
        elif num_roles == 1:
            return 0.8
        else:
            return 0.4
