package com.internmatch.backend.repository;

import com.internmatch.backend.entity.RecommendationBatch;
import com.internmatch.backend.entity.Resume;
import com.internmatch.backend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RecommendationBatchRepository extends JpaRepository<RecommendationBatch, Integer> {

    List<RecommendationBatch> findByUser(User user);
    List<RecommendationBatch> findByResume(Resume resume);
    List<RecommendationBatch> findByResumeOrderByGeneratedAtDesc(Resume resume);
}
