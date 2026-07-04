package com.internmatch.backend.dto;

import com.internmatch.backend.entity.ProcessingStatus;
import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@Builder
public class ResumeResponse {

    private Long resumeId;
    private Integer userId;
    private String fileName;
    private String filePath;
    private Long fileSize;
    private String mimeType;
    private LocalDateTime uploadedAt;
    private ProcessingStatus processingStatus;
    private Boolean embeddingGenerated;
}