import time
from typing import List, Tuple, Dict, Any
from embedding.models import ResumeEmbedding, InternshipEmbedding
from embedding.model_manager import ModelManager
from embedding.repository import EmbeddingRepository
from embedding.input_builder import EmbeddingInputBuilder

class EmbeddingService:
    def __init__(self, model_manager: ModelManager, repository: EmbeddingRepository):
        self.model_manager = model_manager
        self.repository = repository
        self.model_name = self.model_manager.model_name

    def generate_resume_embedding(self, resume_id: int, normalized_resume: Dict[str, Any]) -> ResumeEmbedding:
        text = EmbeddingInputBuilder.build_resume_text(normalized_resume)
        model = self.model_manager.get_model()
        vector = model.encode(text).tolist()
        
        embedding = ResumeEmbedding(
            resume_id=resume_id,
            model_name=self.model_name,
            embedding=vector,
            created_at=time.time()
        )
        self.repository.save_resume_embedding(embedding)
        return embedding

    def generate_internship_embedding(self, internship_id: int, normalized_internship: Dict[str, Any]) -> InternshipEmbedding:
        text = EmbeddingInputBuilder.build_internship_text(normalized_internship)
        model = self.model_manager.get_model()
        vector = model.encode(text).tolist()
        
        embedding = InternshipEmbedding(
            internship_id=internship_id,
            model_name=self.model_name,
            embedding=vector,
            created_at=time.time()
        )
        self.repository.save_internship_embedding(embedding)
        return embedding

    def generate_internships_batch(self, internships: List[Tuple[int, Dict[str, Any]]]) -> List[InternshipEmbedding]:
        if not internships:
            return []
            
        texts = []
        ids = []
        for internship_id, norm_internship in internships:
            texts.append(EmbeddingInputBuilder.build_internship_text(norm_internship))
            ids.append(internship_id)
            
        model = self.model_manager.get_model()
        vectors = model.encode(texts).tolist()
        
        embeddings = []
        for i, vector in enumerate(vectors):
            emb = InternshipEmbedding(
                internship_id=ids[i],
                model_name=self.model_name,
                embedding=vector,
                created_at=time.time()
            )
            self.repository.save_internship_embedding(emb)
            embeddings.append(emb)
            
        return embeddings
