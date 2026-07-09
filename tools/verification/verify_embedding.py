import sys
import os
import time
import psutil
import math

# Add ai-service to path
sys.path.append("d:\\PROJECTS\\Internship-recommendation-engine\\ai-service")

from embedding.model_manager import ModelManager
from embedding.repository import InMemoryEmbeddingRepository
from embedding.service import EmbeddingService
from embedding.input_builder import EmbeddingInputBuilder

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024) # Return MB

def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def magnitude(v):
    return math.sqrt(sum(a * a for a in v))

def cosine_similarity(v1, v2):
    mag1 = magnitude(v1)
    mag2 = magnitude(v2)
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product(v1, v2) / (mag1 * mag2)

def test_pipeline():
    print("=== SPRINT 15 EMBEDDING PIPELINE VERIFICATION ===")
    
    # 1. Verify Input Builder
    print("\n[Test 1] Verifying EmbeddingInputBuilder...")
    mock_resume = {
        "skills": {"normalized": ["Python", "Spring Boot", "SQL", "Docker"]},
        "education": {"normalized": ["Bachelor of Engineering in Computer Science"]},
        "companies": {"normalized": ["Software Development Intern at ABC Technologies"]},
        "projects": {"normalized": ["AI Internship Recommendation System"]},
        "certifications": {"normalized": ["AWS Cloud Practitioner"]}
    }
    
    formatted_resume = EmbeddingInputBuilder.build_resume_text(mock_resume)
    print("--- Human Readable Formatted Resume ---")
    print(formatted_resume)
    print("---------------------------------------")
    
    # Verify identical inputs produce identical formatted text
    formatted_resume_dup = EmbeddingInputBuilder.build_resume_text(mock_resume)
    assert formatted_resume == formatted_resume_dup, "Formatted text is not deterministic!"
    
    # Verify missing sections are skipped cleanly and whitespace is correct
    partial_resume = {
        "skills": {"normalized": ["Python"]},
        "education": {"normalized": []},
        "companies": {"normalized": []},
        "projects": {"normalized": ["My Project"]}
    }
    formatted_partial = EmbeddingInputBuilder.build_resume_text(partial_resume)
    print("--- Human Readable Formatted Partial Resume ---")
    print(formatted_partial)
    print("-----------------------------------------------")
    assert "Education" not in formatted_partial, "Missing section was not skipped cleanly!"
    assert "Experience" not in formatted_partial, "Missing section was not skipped cleanly!"
    assert formatted_partial == "Skills:\nPython\n\nProjects:\nMy Project", "Whitespace or formatting mismatch!"
    print("-> EmbeddingInputBuilder verified successfully.")
    
    # 2. Measure Memory Usage Before Load
    mem_before = get_memory_usage()
    print(f"\nMemory usage before loading model: {mem_before:.2f} MB")
    
    # 3. Verify Singleton Pattern
    print("\n[Test 2] Verifying ModelManager is a Singleton...")
    t0 = time.time()
    manager1 = ModelManager()
    t1 = time.time()
    load_time = t1 - t0
    print(f"Time taken to load model first time: {load_time:.4f} seconds")
    
    manager2 = ModelManager()
    assert id(manager1) == id(manager2), "ModelManager is NOT a singleton!"
    print("-> ModelManager singleton verified successfully (Both handles refer to the exact same instance).")
    
    mem_after = get_memory_usage()
    print(f"Memory usage after loading model: {mem_after:.2f} MB")
    print(f"Net memory consumed by model: {mem_after - mem_before:.2f} MB")
    
    # Initialize service and repo
    repo = InMemoryEmbeddingRepository()
    service = EmbeddingService(manager1, repo)
    
    # 4. Verify single embedding generation dimension & metadata
    print("\n[Test 3] Verifying Single Embedding Generation & Metadata...")
    t0 = time.time()
    resume_emb = service.generate_resume_embedding(resume_id=1, normalized_resume=mock_resume)
    t_single = time.time() - t0
    
    print(f"Embedding Vector Dimension: {len(resume_emb.embedding)}")
    print(f"Model Name Metadata: {resume_emb.model_name}")
    print(f"Timestamp: {resume_emb.created_at}")
    print(f"Time taken for single embedding generation: {t_single * 1000:.2f} ms")
    
    assert len(resume_emb.embedding) == 384, f"Vector length expected to be 384, got {len(resume_emb.embedding)}"
    assert resume_emb.model_name == "all-MiniLM-L6-v2", "Model name mismatch"
    print("-> Single embedding and metadata verified.")
    
    # 5. Verify Identity and Cosine Similarity
    print("\n[Test 4] Verifying Cosine Similarity & Identity...")
    resume_emb2 = service.generate_resume_embedding(resume_id=2, normalized_resume=mock_resume)
    
    # Similarity with itself
    self_sim = cosine_similarity(resume_emb.embedding, resume_emb.embedding)
    print(f"Cosine similarity with itself: {self_sim:.6f}")
    assert abs(self_sim - 1.0) < 1e-5, f"Similarity should be close to 1.0, got {self_sim}"
    
    # Similarity with identical input
    identical_sim = cosine_similarity(resume_emb.embedding, resume_emb2.embedding)
    print(f"Cosine similarity with identical inputs: {identical_sim:.6f}")
    assert abs(identical_sim - 1.0) < 1e-5, f"Similarity should be close to 1.0, got {identical_sim}"
    assert resume_emb.embedding == resume_emb2.embedding, "Identical inputs produced different embeddings"
    print("-> Cosine similarity and identity verified.")
    
    # 6. Verify Batch Embedding Generation
    print("\n[Test 5] Verifying Batch Ingestion...")
    mock_internships = [
        (10, {"title": "Software Engineer", "company": "Google", "description": "Backend services", "required_skills": "Python"}),
        (20, {"title": "Data Analyst", "company": "Amazon", "description": "SQL and scripting", "required_skills": "Python, SQL"}),
        (30, {"title": "Frontend Engineer", "company": "Meta", "description": "React components", "required_skills": "React"})
    ]
    
    t0 = time.time()
    batch_embs = service.generate_internships_batch(mock_internships)
    t_batch = time.time() - t0
    print(f"Time taken to generate batch of {len(mock_internships)} internships: {t_batch * 1000:.2f} ms")
    print(f"Average time per internship in batch: {(t_batch / len(mock_internships)) * 1000:.2f} ms")
    
    assert len(batch_embs) == len(mock_internships), "Batch output length mismatch"
    for i, emb in enumerate(batch_embs):
        assert len(emb.embedding) == 384, f"Batch item {i} vector length mismatch"
        assert emb.model_name == "all-MiniLM-L6-v2", f"Batch item {i} model name mismatch"
        
    print("-> Batch embedding generation verified.")

if __name__ == "__main__":
    test_pipeline()
