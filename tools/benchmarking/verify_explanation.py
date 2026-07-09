import sys
import os
import time

sys.path.append("d:\\PROJECTS\\Internship-recommendation-engine\\ai-service")

from recommendation.models import RecommendationResult
from recommendation.explanation.service import ExplainableRecommendationService

def test_explanation():
    print("=== SPRINT 18 EXPLAINABLE AI VERIFICATION ===")
    
    service = ExplainableRecommendationService()
    
    # Mock Normalized Resume
    mock_resume = {
        "skills": {"normalized": ["Python", "Spring Boot", "SQL"]},
        "education": {"normalized": ["Bachelor of Engineering"]},
        "companies": {"normalized": ["ABC Corp"]},
        "projects": {"normalized": []},
        "certifications": {"normalized": []}
    }
    
    # Mock Internship
    mock_internship = {
        "internship_id": 1,
        "title": "Software Engineer Intern",
        "company": "Google",
        "required_skills": "Python, Docker, SQL",
        "eligibility": "Bachelor",
        "location": "Mountain View",
        "mode": "ONLINE"
    }
    
    # Mock RecommendationResult
    mock_result = RecommendationResult(
        internship_id=1,
        title="Software Engineer Intern",
        company="Google",
        semantic_score=0.8,
        skill_score=0.6667,
        education_score=1.0,
        experience_score=0.8,
        eligibility_score=1.0,
        final_score=0.8067
    )
    
    t0 = time.perf_counter()
    explanation = service.generate_explanation(mock_result, mock_resume, mock_internship)
    latency = (time.perf_counter() - t0) * 1000
    
    # 1. Output Structured Data Check
    print("\n[Test 1] Verifying Structured Explanation Output...")
    print(f"Overall Score: {explanation.overall_score}")
    print(f"Matched Skills: {explanation.matched_skills}")
    print(f"Missing Skills: {explanation.missing_skills}")
    print(f"Matched Education: {explanation.matched_education}")
    print(f"Eligibility Status: {explanation.eligibility_status}")
    print(f"Score Breakdown: {explanation.score_breakdown}")
    print(f"Explanation Text:\n\"{explanation.explanation_text}\"")
    
    assert explanation.internship_id == 1
    assert "Python" in explanation.matched_skills
    assert "sql" in [s.lower() for s in explanation.matched_skills]
    assert "Docker" in explanation.missing_skills
    assert "Bachelor of Engineering" in explanation.matched_education
    assert explanation.eligibility_status is True
    print("-> Structured data verified successfully.")
    
    # 2. Verify Score Breakdown Sum
    print("\n[Test 2] Verifying Score Breakdown Alignment...")
    breakdown_sum = sum(explanation.score_breakdown.values())
    print(f"Sum of weighted scores in breakdown: {breakdown_sum:.4f} (Expected: {mock_result.final_score})")
    assert abs(breakdown_sum - mock_result.final_score) < 1e-3, "Breakdown sum does not match final score!"
    print("-> Score breakdown check passed.")
    
    # 3. Verify Determinism
    print("\n[Test 3] Verifying Determinism...")
    explanation_dup = service.generate_explanation(mock_result, mock_resume, mock_internship)
    assert explanation.explanation_text == explanation_dup.explanation_text, "Explanations are not deterministic!"
    assert explanation.score_breakdown == explanation_dup.score_breakdown, "Breakdowns are not deterministic!"
    print("-> Explanations are fully deterministic.")
    
    # 4. Latency
    print(f"\n[Test 4] Performance Benchmarks...")
    print(f"Explanation Generation Latency: {latency:.4f} ms")
    
if __name__ == "__main__":
    test_explanation()
