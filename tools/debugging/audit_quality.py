import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # No, wait, __file__ is the scratch folder!
sys.path.append(r"d:\PROJECTS\Internship-recommendation-engine\ai-service")
import json
import mysql.connector

# Import pipeline components
from resume.parser import ResumeParser
from nlp.repository import SkillsRepository
from normalization.normalizer import ResumeNormalizer
from normalization.canonical_dictionary import CanonicalDictionary
from embedding.model_manager import ModelManager
from embedding.repository import InMemoryEmbeddingRepository
from embedding.service import EmbeddingService
from similarity.service import SimilarityService
from recommendation.engine import RecommendationEngine
from dataset.pipeline import IngestionPipeline

print("=== STARTING RECOMMENDATION QUALITY AUDIT ===")

skills_repo = SkillsRepository()
parser = ResumeParser(skills_repo)
canonical_dict = CanonicalDictionary()
normalizer = ResumeNormalizer(canonical_dict)
model_manager = ModelManager()
embedding_repo = InMemoryEmbeddingRepository()
embedding_service = EmbeddingService(model_manager, embedding_repo)
similarity_service = SimilarityService()
rec_engine = RecommendationEngine()

resume_text = """
John Doe
Location: New York, NY
Email: john@example.com

Education:
B.S. in Computer Science, Stanford University (Expected 2025)
CGPA: 3.8/4.0

Skills:
Languages: Python, Java, JavaScript, TypeScript
Frameworks: React, Node.js, Spring Boot
Tools: Git, Docker, AWS, SQL, MongoDB

Experience:
Software Engineering Intern at TechCorp
- Developed a RESTful API using Node.js and Express
- Built a frontend dashboard using React and Tailwind CSS
- Improved database query performance by 20% using SQL indexing

Projects:
- Personal Portfolio: A responsive web app built with React
- E-commerce backend: A microservices architecture using Spring Boot and Docker
"""

print("\n1. Parsing and Normalizing Resume...")
parse_result = parser.parse(resume_text)
norm_resume = normalizer.normalize(parse_result)
print(f"Resume Skills Extracted: {norm_resume.get('skills', [])}")

print("\n2. Generating Resume Embedding...")
from embedding.input_builder import EmbeddingInputBuilder
resume_input_text = EmbeddingInputBuilder.build_resume_text(norm_resume)
print(f"Resume Embedding Input Text:\n{resume_input_text}\n")
resume_emb = embedding_service.generate_resume_embedding(1, norm_resume)

print("Fetching internships from database...")
pipeline = IngestionPipeline()
conn = mysql.connector.connect(**pipeline.db_config)
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM internships")
internships = cursor.fetchall()
cursor.close()
conn.close()

internship_tuples = []
internship_map = {}
for item in internships:
    iid = item.get("internship_id")
    internship_tuples.append((iid, item))
    internship_map[iid] = item

print("Generating internship embeddings...")
internship_embs = embedding_service.generate_internships_batch(internship_tuples)

print("\n3. Calculating Top 10 Cosine Similarity Scores...")
similarity_matches = similarity_service.compare_resume_to_internships(
    resume_emb, internship_embs, top_k=10
)
for idx, match in enumerate(similarity_matches):
    title = internship_map[match.internship_id].get("title", "")
    print(f"Rank {idx+1}: Internship ID {match.internship_id} ({title}) - Cosine Similarity: {match.similarity_score:.4f}")

print("\n4. Running Recommendation Engine (Scorers)...")
rec_results = rec_engine.rank_recommendations(
    norm_resume, similarity_matches, internships, top_n=10
)

print("\n--- Recommendation Weights (Sprint 17 Config) ---")
for scorer in rec_engine.scorers:
    print(f"{scorer.__class__.__name__}: {scorer.weight}")

print("\n--- Final Recommendation Output ---")
for idx, res in enumerate(rec_results):
    print(f"\nRecommendation Rank {idx+1}: {res.title} at {res.company}")
    print(f"   Final Weighted Score: {res.final_score:.4f}")
    print(f"   Semantic Score: {res.semantic_score:.4f}")
    print(f"   Skill Score: {res.skill_score:.4f}")
    print(f"   Education Score: {res.education_score:.4f}")
    print(f"   Experience Score: {res.experience_score:.4f}")
    print(f"   Eligibility Score: {res.eligibility_score:.4f}")

print("\n=== AUDIT COMPLETE ===")
