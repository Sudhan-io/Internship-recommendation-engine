from abc import ABC, abstractmethod
from typing import List, Optional
from embedding.models import ResumeEmbedding, InternshipEmbedding

class EmbeddingRepository(ABC):
    @abstractmethod
    def save_resume_embedding(self, embedding: ResumeEmbedding) -> None:
        pass

    @abstractmethod
    def get_resume_embedding(self, resume_id: int) -> Optional[ResumeEmbedding]:
        pass

    @abstractmethod
    def save_internship_embedding(self, embedding: InternshipEmbedding) -> None:
        pass

    @abstractmethod
    def get_internship_embedding(self, internship_id: int) -> Optional[InternshipEmbedding]:
        pass

    @abstractmethod
    def get_all_internship_embeddings(self) -> List[InternshipEmbedding]:
        pass

class InMemoryEmbeddingRepository(EmbeddingRepository):
    def __init__(self):
        self.resume_embeddings = {}
        self.internship_embeddings = {}

    def save_resume_embedding(self, embedding: ResumeEmbedding) -> None:
        self.resume_embeddings[embedding.resume_id] = embedding

    def get_resume_embedding(self, resume_id: int) -> Optional[ResumeEmbedding]:
        return self.resume_embeddings.get(resume_id)

    def save_internship_embedding(self, embedding: InternshipEmbedding) -> None:
        self.internship_embeddings[embedding.internship_id] = embedding

    def get_internship_embedding(self, internship_id: int) -> Optional[InternshipEmbedding]:
        return self.internship_embeddings.get(internship_id)

    def get_all_internship_embeddings(self) -> List[InternshipEmbedding]:
        return list(self.internship_embeddings.values())
