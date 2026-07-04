from typing import List, Dict, Any
from recommendation.models import RecommendationResult
from recommendation.scorers.base import Scorer
from recommendation.scorers.semantic import SemanticScorer
from recommendation.scorers.skill import SkillScorer
from recommendation.scorers.education import EducationScorer
from recommendation.scorers.experience import ExperienceScorer
from recommendation.scorers.eligibility import EligibilityScorer
from similarity.models import SimilarityResult

class RecommendationEngine:
    def __init__(self):
        self.scorers: List[Scorer] = [
            SemanticScorer(),
            SkillScorer(),
            EducationScorer(),
            ExperienceScorer(),
            EligibilityScorer()
        ]
        total_weight = sum(scorer.weight for scorer in self.scorers)
        assert abs(total_weight - 1.0) < 1e-5, f"Scorer weights must sum to 1.0, got {total_weight}"

    def rank_recommendations(
        self, 
        normalized_resume: Dict[str, Any], 
        top_similarity_matches: List[SimilarityResult], 
        internships_metadata: List[Dict[str, Any]],
        top_n: int = 10
    ) -> List[RecommendationResult]:
        internship_map = {item["internship_id"]: item for item in internships_metadata}
        
        results = []
        for match in top_similarity_matches:
            internship_id = match.internship_id
            if internship_id not in internship_map:
                continue
                
            internship = internship_map[internship_id]
            similarity_score = match.similarity_score
            
            scores = {}
            final_score = 0.0
            
            for scorer in self.scorers:
                name = scorer.__class__.__name__.replace("Scorer", "").lower()
                score = scorer.calculate_score(normalized_resume, internship, similarity_score)
                score = max(0.0, min(1.0, score))
                scores[name] = score
                final_score += score * scorer.weight
                
            results.append(
                RecommendationResult(
                    internship_id=internship_id,
                    title=internship.get("title", ""),
                    company=internship.get("company", "") or internship.get("company_name", ""),
                    semantic_score=round(scores.get("semantic", 0.0), 4),
                    skill_score=round(scores.get("skill", 0.0), 4),
                    education_score=round(scores.get("education", 0.0), 4),
                    experience_score=round(scores.get("experience", 0.0), 4),
                    eligibility_score=round(scores.get("eligibility", 0.0), 4),
                    final_score=round(final_score, 4)
                )
            )
            
        results.sort(key=lambda x: x.final_score, reverse=True)
        return results[:top_n]
