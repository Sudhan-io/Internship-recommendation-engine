import sys
import os
import time
import random

sys.path.append("d:\\PROJECTS\\Internship-recommendation-engine\\ai-service")

from embedding.models import ResumeEmbedding, InternshipEmbedding
from similarity.service import SimilarityService
from similarity.utils import calculate_cosine_similarity

def test_similarity():
    print("=== SPRINT 16 SIMILARITY ENGINE VERIFICATION ===")
    
    service = SimilarityService()
    
    # 1. Identity Verification
    print("\n[Test 1] Verifying Identical & Unrelated Embeddings...")
    # 384 dimensional vectors
    vec_a = [random.uniform(-1, 1) for _ in range(384)]
    # Normalize vec_a to make it realistic
    norm_a = sum(x*x for x in vec_a)**0.5
    vec_a = [x/norm_a for x in vec_a]
    
    vec_b = [x for x in vec_a] # Identical
    
    # Unrelated vector (random orthogonalish)
    vec_c = [random.uniform(-1, 1) for _ in range(384)]
    norm_c = sum(x*x for x in vec_c)**0.5
    vec_c = [x/norm_c for x in vec_c]
    
    sim_self = calculate_cosine_similarity(vec_a, vec_b)
    sim_unrelated = calculate_cosine_similarity(vec_a, vec_c)
    
    print(f"Cosine similarity with identical vector: {sim_self:.6f}")
    print(f"Cosine similarity with random vector: {sim_unrelated:.6f}")
    
    assert abs(sim_self - 1.0) < 1e-5, f"Expected ~1.0, got {sim_self}"
    assert abs(sim_unrelated) < 0.5, f"Expected low similarity, got {sim_unrelated}"
    print("-> Identity check passed.")
    
    # 2. Top-K and Sorting Verification
    print("\n[Test 2] Verifying Top-K and Descending Sorting...")
    resume_emb = ResumeEmbedding(resume_id=1, model_name="test-model", embedding=vec_a, created_at=time.time())
    
    # Generate 150 mock internship embeddings with random vectors
    internship_embs = []
    for i in range(150):
        # Create vectors with increasing distance
        # To make it deterministic, let's interpolate between vec_a and random vectors
        factor = i / 150.0
        rand_v = [random.uniform(-1, 1) for _ in range(384)]
        norm_r = sum(x*x for x in rand_v)**0.5
        rand_v = [x/norm_r for x in rand_v]
        
        interp = [(1 - factor)*x + factor*y for x, y in zip(vec_a, rand_v)]
        norm_i = sum(x*x for x in interp)**0.5
        v = [x/norm_i for x in interp]
        
        internship_embs.append(
            InternshipEmbedding(
                internship_id=i,
                model_name="test-model",
                embedding=v,
                created_at=time.time()
            )
        )
        
    t0 = time.time()
    results = service.compare_resume_to_internships(resume_emb, internship_embs, top_k=100)
    latency = time.time() - t0
    
    print(f"Compared resume to {len(internship_embs)} internships.")
    print(f"Top-K results returned: {len(results)} (expected: 100)")
    print(f"Top 100 retrieval execution time: {latency * 1000:.4f} ms")
    
    assert len(results) == 100, f"Expected 100 results, got {len(results)}"
    
    # Check descending sort order
    for idx in range(len(results) - 1):
        score_current = results[idx].similarity_score
        score_next = results[idx + 1].similarity_score
        assert score_current >= score_next, f"Descending sort order violated at index {idx}: {score_current} < {score_next}"
        
    print("-> Sorting and Top-K verified successfully.")
    
    # 3. Latency benchmarks
    print("\n[Test 3] Latency Benchmarking (Batch Comparison Sizes)...")
    
    def benchmark_size(num_items):
        test_embs = []
        for i in range(num_items):
            rand_v = [random.uniform(-1, 1) for _ in range(384)]
            norm_r = sum(x*x for x in rand_v)**0.5
            test_embs.append(
                InternshipEmbedding(
                    internship_id=i,
                    model_name="test-model",
                    embedding=[x/norm_r for x in rand_v],
                    created_at=time.time()
                )
            )
        # Measure
        t_start = time.perf_counter()
        _ = service.compare_resume_to_internships(resume_emb, test_embs, top_k=100)
        t_end = time.perf_counter()
        return (t_end - t_start) * 1000
        
    for size in [100, 500, 1000, 5000, 10000]:
        time_ms = benchmark_size(size)
        print(f"  - Size {size:5d}: {time_ms:6.2f} ms")
        
    print("-> Benchmark completed successfully.")

if __name__ == "__main__":
    test_similarity()
