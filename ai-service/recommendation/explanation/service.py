import re
from typing import Dict, Any
from recommendation.models import RecommendationResult
from recommendation.explanation.models import RecommendationExplanation
from recommendation.explanation.formatter import ExplanationFormatter

class ExplainableRecommendationService:
    def generate_explanation(
        self, 
        result: RecommendationResult, 
        normalized_resume: Dict[str, Any], 
        internship: Dict[str, Any]
    ) -> RecommendationExplanation:
        resume_skills = [s.lower().strip() for s in normalized_resume.get("skills", {}).get("normalized", [])]
        resume_skills_original_case = {s.lower().strip(): s for s in normalized_resume.get("skills", {}).get("normalized", [])}
        
        req_skills_raw = internship.get("required_skills", "")
        if isinstance(req_skills_raw, list):
            req_skills = [s.lower().strip() for s in req_skills_raw if s.strip()]
        else:
            req_skills = [s.lower().strip() for s in re.split(r",|;|/|\s+and\s+", str(req_skills_raw)) if s.strip()]
            
        matched_skills_lower = [s for s in req_skills if s in resume_skills]
        missing_skills_lower = [s for s in req_skills if s not in resume_skills]
        
        matched_skills = [resume_skills_original_case.get(s, s.capitalize()) for s in matched_skills_lower]
        missing_skills = [s.capitalize() for s in missing_skills_lower]
        
        resume_edu = normalized_resume.get("education", {}).get("normalized", [])
        eligibility = str(internship.get("eligibility", "")).lower()
        
        matched_edu = []
        missing_edu = []
        
        if eligibility:
            for edu in resume_edu:
                if "bachelor" in edu.lower() or "b.e" in edu.lower() or "b.tech" in edu.lower():
                    if "bachelor" in eligibility or "b.e" in eligibility or "b.tech" in eligibility:
                        matched_edu.append(edu)
                if "master" in edu.lower() or "m.s" in edu.lower() or "m.tech" in edu.lower():
                    if "master" in eligibility or "m.s" in eligibility or "m.tech" in eligibility:
                        matched_edu.append(edu)
            if not matched_edu and ("bachelor" in eligibility or "master" in eligibility or "phd" in eligibility):
                missing_edu.append(internship.get("eligibility", ""))
        else:
            matched_edu = resume_edu
            
        companies = normalized_resume.get("companies", {}).get("normalized", [])
        matched_exp = companies
        
        eligibility_status = result.eligibility_score > 0.4
        
        score_breakdown = {
            "semantic_similarity": round(result.semantic_score * 0.45, 4),
            "skill_match": round(result.skill_score * 0.25, 4),
            "education_match": round(result.education_score * 0.15, 4),
            "experience_match": round(result.experience_score * 0.10, 4),
            "eligibility_match": round(result.eligibility_score * 0.05, 4)
        }
        
        explanation_text = ExplanationFormatter.format_explanation(
            result.final_score,
            matched_skills,
            missing_skills,
            matched_edu,
            eligibility_status
        )
        
        return RecommendationExplanation(
            internship_id=result.internship_id,
            overall_score=result.final_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            matched_education=matched_edu,
            missing_education=missing_edu,
            matched_experience=matched_exp,
            eligibility_status=eligibility_status,
            score_breakdown=score_breakdown,
            explanation_text=explanation_text
        )
