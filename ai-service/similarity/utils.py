import numpy as np
from typing import List

def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    a = np.array(vec1)
    b = np.array(vec2)
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(dot / (norm_a * norm_b))

def calculate_cosine_similarities_batch(query_vec: List[float], target_vecs: List[List[float]]) -> List[float]:
    if not target_vecs:
        return []
    q = np.array(query_vec)
    targets = np.array(target_vecs)
    
    q_norm = np.linalg.norm(q)
    if q_norm == 0.0:
        return [0.0] * len(target_vecs)
    q = q / q_norm
    
    target_norms = np.linalg.norm(targets, axis=1)
    target_norms[target_norms == 0.0] = 1.0
    targets_normed = targets / target_norms[:, np.newaxis]
    
    similarities = np.dot(targets_normed, q)
    return similarities.tolist()
