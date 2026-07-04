from recommendation.scorers.base import Scorer
from typing import Dict, Any

class EducationScorer(Scorer):
    @property
    def weight(self) -> float:
        return 0.15

    def calculate_score(self, resume: Dict[str, Any], internship: Dict[str, Any], similarity_score: float) -> float:
        resume_edu = [e.lower() for e in resume.get("education", {}).get("normalized", [])]
        eligibility = str(internship.get("eligibility", "")).lower()
        
        if not eligibility:
            return 1.0
            
        req_degrees = []
        if "phd" in eligibility or "doctor" in eligibility:
            req_degrees.append("doctor")
        if "master" in eligibility or "m.s" in eligibility or "m.tech" in eligibility or "postgrad" in eligibility:
            req_degrees.append("master")
        if "bachelor" in eligibility or "b.e" in eligibility or "b.tech" in eligibility or "undergrad" in eligibility:
            req_degrees.append("bachelor")
            
        if not req_degrees:
            return 1.0
            
        candidate_degrees = []
        for edu in resume_edu:
            if "doctor" in edu or "ph.d" in edu:
                candidate_degrees.append("doctor")
            if "master" in edu or "m.s" in edu or "m.tech" in edu:
                candidate_degrees.append("master")
            if "bachelor" in edu or "b.e" in edu or "b.tech" in edu:
                candidate_degrees.append("bachelor")
                
        if not candidate_degrees:
            return 0.0
            
        level_hierarchy = {"doctor": 3, "master": 2, "bachelor": 1}
        max_candidate_level = max(level_hierarchy.get(d, 0) for d in candidate_degrees)
        max_required_level = max(level_hierarchy.get(d, 0) for d in req_degrees)
        
        if max_candidate_level >= max_required_level:
            return 1.0
        elif max_candidate_level > 0:
            return 0.5
        return 0.0
