from dataclasses import dataclass
from typing import List, Dict

@dataclass
class RecommendationExplanation:
    internship_id: int
    overall_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    matched_education: List[str]
    missing_education: List[str]
    matched_experience: List[str]
    eligibility_status: bool
    score_breakdown: Dict[str, float]
    explanation_text: str
