from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import mysql.connector

from resume.parser import ResumeParser
from nlp.repository import SkillsRepository
from normalization.normalizer import ResumeNormalizer
from normalization.canonical_dictionary import CanonicalDictionary
from embedding.model_manager import ModelManager
from embedding.repository import InMemoryEmbeddingRepository
from embedding.service import EmbeddingService
from similarity.service import SimilarityService
from recommendation.engine import RecommendationEngine
from recommendation.explanation.service import ExplainableRecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendation"])

skills_repo = SkillsRepository()
parser = ResumeParser(skills_repo)
canonical_dict = CanonicalDictionary()
normalizer = ResumeNormalizer(canonical_dict)
model_manager = ModelManager()
embedding_repo = InMemoryEmbeddingRepository()
embedding_service = EmbeddingService(model_manager, embedding_repo)
similarity_service = SimilarityService()
rec_engine = RecommendationEngine()
explain_service = ExplainableRecommendationService()

class RecommendationRequest(BaseModel):
    resume_text: str
    internships: Optional[List[Dict[str, Any]]] = None

@router.post("/generate")
def generate_recommendations(req: RecommendationRequest):
    try:
        parse_result = parser.parse(req.resume_text)
        norm_resume = normalizer.normalize(parse_result)
        resume_emb = embedding_service.generate_resume_embedding(1, norm_resume)
        
        internships = req.internships
        if not internships:
            from dataset.pipeline import IngestionPipeline
            pipeline = IngestionPipeline()
            conn = None
            cursor = None
            try:
                conn = mysql.connector.connect(**pipeline.db_config)
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM internships")
                internships = cursor.fetchall()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        
        if not internships:
            return {"recommendations": []}
            
        internship_tuples = []
        for item in internships:
            iid = item.get("internship_id") or item.get("internshipId")
            internship_tuples.append((iid, item))
            
        internship_embs = embedding_service.generate_internships_batch(internship_tuples)
        
        similarity_matches = similarity_service.compare_resume_to_internships(
            resume_emb, internship_embs, top_k=100
        )
        
        rec_results = rec_engine.rank_recommendations(
            norm_resume, similarity_matches, internships, top_n=10
        )
        
        internship_map = {item.get("internship_id") or item.get("internshipId"): item for item in internships}
        
        recommendations_with_explanations = []
        for res in rec_results:
            internship_item = internship_map.get(res.internship_id)
            explanation = explain_service.generate_explanation(
                res, norm_resume, internship_item
            )
            recommendations_with_explanations.append({
                "internship_id": res.internship_id,
                "title": res.title,
                "company": res.company,
                "location": internship_item.get("location", ""),
                "mode": internship_item.get("mode", ""),
                "description": internship_item.get("description", ""),
                "required_skills": internship_item.get("required_skills", ""),
                "eligibility": internship_item.get("eligibility", ""),
                "apply_url": internship_item.get("apply_url", ""),
                "final_score": res.final_score,
                "score_breakdown": {
                    "semantic_similarity": res.semantic_score,
                    "skill_match": res.skill_score,
                    "education_match": res.education_score,
                    "experience_match": res.experience_score,
                    "eligibility_match": res.eligibility_score
                },
                "matched_skills": explanation.matched_skills,
                "missing_skills": explanation.missing_skills,
                "matched_education": explanation.matched_education,
                "missing_education": explanation.missing_education,
                "matched_experience": explanation.matched_experience,
                "eligibility_status": explanation.eligibility_status,
                "explanation_text": explanation.explanation_text
            })
            
        return {
            "status": "success",
            "model_name": "all-MiniLM-L6-v2",
            "recommendations": recommendations_with_explanations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
