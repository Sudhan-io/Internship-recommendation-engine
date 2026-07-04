from recommendation.scorers.base import Scorer
from typing import Dict, Any

class EligibilityScorer(Scorer):
    @property
    def weight(self) -> float:
        return 0.05

    def calculate_score(self, resume: Dict[str, Any], internship: Dict[str, Any], similarity_score: float) -> float:
        mode = str(internship.get("mode", "")).upper()
        if mode == "ONLINE":
            return 1.0
            
        candidate_text = " ".join([
            " ".join(resume.get("education", {}).get("original", [])),
            " ".join(resume.get("companies", {}).get("original", []))
        ]).lower()
        
        intern_loc = str(internship.get("location", "")).lower()
        if not intern_loc or intern_loc == "unspecified":
            return 1.0
            
        loc_words = [w.strip() for w in intern_loc.split(",") if len(w.strip()) > 2]
        if any(w in candidate_text for w in loc_words):
            return 1.0
            
        if mode == "HYBRID":
            return 0.5
        return 0.2
