from dataclasses import dataclass

@dataclass
class RecommendationResult:
    internship_id: int
    title: str
    company: str
    semantic_score: float
    skill_score: float
    education_score: float
    experience_score: float
    eligibility_score: float
    final_score: float
