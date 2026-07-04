package com.internmatch.backend.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "recommendation_batches")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RecommendationBatch {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer batchId;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne
    @JoinColumn(name = "resume_id", nullable = false)
    private Resume resume;

    private String modelName;

    private Integer recommendationCount;

    private LocalDateTime generatedAt;
}
