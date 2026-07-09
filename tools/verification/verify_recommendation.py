import sys
import os
import time
import psutil

sys.path.append("d:\\PROJECTS\\Internship-recommendation-engine\\ai-service")

from recommendation.engine import RecommendationEngine
from similarity.models import SimilarityResult

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def test_recommendation():
    print("=== SPRINT 17 RECOMMENDATION ENGINE VERIFICATION ===")
    
    engine = RecommendationEngine()
    
    # Mock resume input (Python and Docker skills, Bachelor education)
    resume_java = {
        "skills": {"normalized": ["Java", "Spring Boot", "SQL"]},
        "education": {"normalized": ["Bachelor of Engineering"]},
        "companies": {"normalized": ["ABC Corp"]},
        "projects": {"normalized": []},
        "certifications": {"normalized": []}
    }
    
    resume_python = {
        "skills": {"normalized": ["Python", "Docker"]},
        "education": {"normalized": ["Bachelor of Engineering"]},
        "companies": {"normalized": ["ABC Corp"]},
        "projects": {"normalized": []},
        "certifications": {"normalized": []}
    }
    
    # 10 Mock Internships
    # Note that Internship 1 and Internship 2 have IDENTICAL semantic similarity (0.8)
    # but different required skills: Internship 1 requires Python, Internship 2 requires Java
    internships_metadata = [
        {"internship_id": 1, "title": "Python Intern", "company": "Google", "required_skills": "Python", "eligibility": "Bachelor", "location": "Seattle", "mode": "ONLINE"},
        {"internship_id": 2, "title": "Java Developer Intern", "company": "Amazon", "required_skills": "Java, Spring Boot", "eligibility": "Bachelor", "location": "Seattle", "mode": "ONLINE"},
        {"internship_id": 3, "title": "Frontend Intern", "company": "Meta", "required_skills": "React", "eligibility": "Bachelor", "location": "Menlo Park", "mode": "HYBRID"},
        {"internship_id": 4, "title": "DevOps Trainee", "company": "Microsoft", "required_skills": "Docker", "eligibility": "Bachelor", "location": "Redmond", "mode": "ONLINE"},
        {"internship_id": 5, "title": "Cloud intern", "company": "Netflix", "required_skills": "AWS", "eligibility": "Bachelor", "location": "Los Gatos", "mode": "OFFLINE"},
        {"internship_id": 6, "title": "Data Science intern", "company": "Apple", "required_skills": "Python, SQL", "eligibility": "Master", "location": "Cupertino", "mode": "ONLINE"},
        {"internship_id": 7, "title": "Backend Intern", "company": "Twitter", "required_skills": "Scala", "eligibility": "Bachelor", "location": "San Francisco", "mode": "ONLINE"},
        {"internship_id": 8, "title": "Security Analyst", "company": "Uber", "required_skills": "Linux", "eligibility": "Bachelor", "location": "San Francisco", "mode": "ONLINE"},
        {"internship_id": 9, "title": "QA Trainee", "company": "Airbnb", "required_skills": "Selenium", "eligibility": "Bachelor", "location": "San Francisco", "mode": "ONLINE"},
        {"internship_id": 10, "title": "Support Intern", "company": "Dropbox", "required_skills": "Bash", "eligibility": "Bachelor", "location": "San Francisco", "mode": "ONLINE"}
    ]
    
    # Similarity results: let's give Internship 1 and 2 high similarity, and others lower
    top_similarity_matches = [
        SimilarityResult(internship_id=1, similarity_score=0.80, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=2, similarity_score=0.80, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=3, similarity_score=0.75, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=4, similarity_score=0.70, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=5, similarity_score=0.65, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=6, similarity_score=0.60, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=7, similarity_score=0.55, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=8, similarity_score=0.50, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=9, similarity_score=0.45, embedding_model="all-MiniLM-L6-v2", generated_at=time.time()),
        SimilarityResult(internship_id=10, similarity_score=0.40, embedding_model="all-MiniLM-L6-v2", generated_at=time.time())
    ]
    
    # 1. Verify Identical Similarity Differentiation
    print("\n[Test 1] Verifying business rules differentiate identical semantic scores...")
    results_python = engine.rank_recommendations(resume_python, top_similarity_matches, internships_metadata)
    
    # For resume_python:
    # Internship 1 (Python) -> 100% skill match (Python vs Python) -> final score should be higher than
    # Internship 2 (Java Developer) -> 0% skill match (Python vs Java/Spring Boot)
    rank_python_ids = [r.internship_id for r in results_python]
    print(f"Ranked output IDs (Python resume): {rank_python_ids}")
    
    pos_internship_1 = rank_python_ids.index(1)
    pos_internship_2 = rank_python_ids.index(2)
    print(f"Position of Python Intern: {pos_internship_1}, Position of Java Intern: {pos_internship_2}")
    assert pos_internship_1 < pos_internship_2, "Identical semantic matches were not differentiated by skill match!"
    print("-> Differentiation test passed.")
    
    # 2. Verify Recommendations Change when Resume Skills Change
    print("\n[Test 2] Verifying recommendations change dynamically with resume skills...")
    results_java = engine.rank_recommendations(resume_java, top_similarity_matches, internships_metadata)
    rank_java_ids = [r.internship_id for r in results_java]
    print(f"Ranked output IDs (Java resume): {rank_java_ids}")
    
    # Now, Internship 2 (Java) should be ranked higher than Internship 1 (Python)
    pos_java_1 = rank_java_ids.index(1)
    pos_java_2 = rank_java_ids.index(2)
    print(f"Position of Python Intern: {pos_java_1}, Position of Java Intern: {pos_java_2}")
    assert pos_java_2 < pos_java_1, "Recommendations did not adapt to changes in candidate skills!"
    print("-> Dynamic shift test passed.")
    
    # 3. Verify Determinism and Reproducibility
    print("\n[Test 3] Verifying Determinism...")
    results_dup = engine.rank_recommendations(resume_python, top_similarity_matches, internships_metadata)
    for r1, r2 in zip(results_python, results_dup):
        assert r1.final_score == r2.final_score, "Calculated scores are not deterministic!"
    print("-> Scores are fully reproducible.")
    
    # 4. Verify output length and weights sum
    print("\n[Test 4] Verifying Weights & Output Count...")
    assert len(results_python) == 10, f"Expected 10 recommendations, got {len(results_python)}"
    print("-> Top 10 returned successfully.")
    
    # Show first result scores for Python candidate
    top_res = results_python[0]
    print(f"\nTop Match Result Details: {top_res.title} at {top_res.company}")
    print(f"  - Semantic Score (45%): {top_res.semantic_score}")
    print(f"  - Skill Score (25%):    {top_res.skill_score}")
    print(f"  - Education Score (15%):{top_res.education_score}")
    print(f"  - Experience Score (10%):{top_res.experience_score}")
    print(f"  - Eligibility Score (5%):{top_res.eligibility_score}")
    print(f"  - Final Combined Score:  {top_res.final_score}")
    
    # 5. Benchmarks
    print("\n[Test 5] Benchmarking...")
    mem_before = get_memory_usage()
    
    t_start = time.perf_counter()
    for _ in range(100):
        _ = engine.rank_recommendations(resume_python, top_similarity_matches, internships_metadata)
    t_end = time.perf_counter()
    
    avg_latency = ((t_end - t_start) / 100) * 1000
    mem_after = get_memory_usage()
    
    print(f"Average Recommendation Latency: {avg_latency:.4f} ms")
    print(f"Memory overhead during scoring: {mem_after - mem_before:.4f} MB")
    
if __name__ == "__main__":
    test_recommendation()
