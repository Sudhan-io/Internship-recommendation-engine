from recommendation.scorers.base import Scorer
from typing import Dict, Any

class SemanticScorer(Scorer):
    @property
    def weight(self) -> float:
        return 0.45

    def calculate_score(self, resume: Dict[str, Any], internship: Dict[str, Any], similarity_score: float) -> float:
        return max(0.0, min(1.0, similarity_score))
