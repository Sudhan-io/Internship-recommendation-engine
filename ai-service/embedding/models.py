from dataclasses import dataclass
from typing import List

@dataclass
class ResumeEmbedding:
    resume_id: int
    model_name: str
    embedding: List[float]
    created_at: float

@dataclass
class InternshipEmbedding:
    internship_id: int
    model_name: str
    embedding: List[float]
    created_at: float
