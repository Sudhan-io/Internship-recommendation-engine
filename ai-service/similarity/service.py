import time
from typing import List
from embedding.models import ResumeEmbedding, InternshipEmbedding
from similarity.models import SimilarityResult
from similarity.utils import calculate_cosine_similarities_batch

class SimilarityService:
    def compare_resume_to_internships(
        self, 
        resume_emb: ResumeEmbedding, 
        internship_embs: List[InternshipEmbedding], 
        top_k: int = 100
    ) -> List[SimilarityResult]:
        if not internship_embs:
            return []
            
        model_name = resume_emb.model_name
        aligned_internships = [emb for emb in internship_embs if emb.model_name == model_name]
        
        if not aligned_internships:
            return []
            
        query_vec = resume_emb.embedding
        target_vecs = [emb.embedding for emb in aligned_internships]
        ids = [emb.internship_id for emb in aligned_internships]
        
        scores = calculate_cosine_similarities_batch(query_vec, target_vecs)
        
        results = []
        for idx, score in enumerate(scores):
            results.append(
                SimilarityResult(
                    internship_id=ids[idx],
                    similarity_score=round(score, 6),
                    embedding_model=model_name,
                    generated_at=time.time()
                )
            )
            
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]
