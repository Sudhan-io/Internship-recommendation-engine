package com.internmatch.backend.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "resumes")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Resume {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long resumeId;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    @Enumerated(EnumType.STRING)
    private ProcessingStatus processingStatus;

    private Boolean embeddingGenerated;
    private String fileName;

    private String filePath;

    private Long fileSize;

    private String mimeType;

    @Lob
    @Column(columnDefinition = "LONGTEXT")
    private String extractedText;

    private LocalDateTime uploadedAt;
}