from dataclasses import dataclass

@dataclass
class SimilarityResult:
    internship_id: int
    similarity_score: float
    embedding_model: str
    generated_at: float
