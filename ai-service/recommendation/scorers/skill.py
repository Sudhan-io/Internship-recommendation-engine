from recommendation.scorers.base import Scorer
from typing import Dict, Any
import re

class SkillScorer(Scorer):
    @property
    def weight(self) -> float:
        return 0.25

    def calculate_score(self, resume: Dict[str, Any], internship: Dict[str, Any], similarity_score: float) -> float:
        resume_skills = set(s.lower() for s in resume.get("skills", {}).get("normalized", []))
        
        req_skills_raw = internship.get("required_skills", "")
        if isinstance(req_skills_raw, list):
            req_skills = [s.lower().strip() for s in req_skills_raw if s.strip()]
        else:
            req_skills = [s.lower().strip() for s in re.split(r",|;|/|\s+and\s+", str(req_skills_raw)) if s.strip()]
            
        if not req_skills:
            return 1.0
            
        matched = [s for s in req_skills if s in resume_skills]
        return len(matched) / len(req_skills)
