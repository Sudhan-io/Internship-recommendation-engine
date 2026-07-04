package com.internmatch.backend.repository;

import com.internmatch.backend.entity.Recommendation;
import com.internmatch.backend.entity.RecommendationBatch;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RecommendationRepository extends JpaRepository<Recommendation, Integer> {

    List<Recommendation> findByBatch(RecommendationBatch batch);
}
