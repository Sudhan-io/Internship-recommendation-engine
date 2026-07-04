package com.internmatch.backend.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "recommendations")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Recommendation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer recommendationId;

    @ManyToOne
    @JoinColumn(name = "batch_id", nullable = false)
    private RecommendationBatch batch;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne
    @JoinColumn(name = "internship_id", nullable = false)
    private Internship internship;

    private Double finalScore;
    private Double semanticScore;
    private Double skillScore;
    private Double educationScore;
    private Double experienceScore;
    private Double eligibilityScore;

    @Lob
    @Column(columnDefinition = "TEXT")
    private String explanationText;

    private String matchedSkills;
    private String missingSkills;
}
