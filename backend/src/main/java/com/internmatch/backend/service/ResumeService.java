package com.internmatch.backend.service;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.ResumeResponse;
import com.internmatch.backend.entity.ProcessingStatus;
import com.internmatch.backend.entity.Resume;
import com.internmatch.backend.entity.User;
import com.internmatch.backend.repository.ResumeRepository;
import lombok.RequiredArgsConstructor;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.UUID;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

@Service
@RequiredArgsConstructor
@Slf4j
public class ResumeService {

    private final ResumeRepository resumeRepository;
    private final Path uploadDir = Paths.get("uploads/resumes");

    public ApiResponse<ResumeResponse> uploadAndExtractResume(MultipartFile file, User user) {
        log.info("User {} uploading resume: {} ({} bytes)", user.getEmail(), file.getOriginalFilename(), file.getSize());

        if (file.isEmpty()) {
            log.warn("Upload failed: File is empty for user {}", user.getEmail());
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "File is empty");
        }

        if (file.getSize() > 5 * 1024 * 1024) {
            log.warn("Upload failed: File size {} exceeds 5MB limit for user {}", file.getSize(), user.getEmail());
            throw new ResponseStatusException(HttpStatus.PAYLOAD_TOO_LARGE, "File size exceeds the maximum limit of 5MB");
        }
        
        String originalFilename = file.getOriginalFilename();
        String contentType = file.getContentType();
        boolean isPdfExtension = originalFilename != null && originalFilename.toLowerCase().endsWith(".pdf");
        boolean isPdfContentType = contentType != null && contentType.equalsIgnoreCase("application/pdf");
        
        if (!isPdfExtension || !isPdfContentType) {
            log.warn("Upload failed: Unsupported file type {} (contentType={}) for user {}", originalFilename, contentType, user.getEmail());
            throw new ResponseStatusException(HttpStatus.UNSUPPORTED_MEDIA_TYPE, "Only PDF files are allowed");
        }

        try {
            if (!Files.exists(uploadDir)) {
                Files.createDirectories(uploadDir);
            }

            String uuid = UUID.randomUUID().toString();
            String uniqueFileName = "resume_" + user.getUserId() + "_" + uuid + ".pdf";
            Path targetPath = uploadDir.resolve(uniqueFileName);

            Files.copy(file.getInputStream(), targetPath);

            String extractedText;
            try (PDDocument document = Loader.loadPDF(targetPath.toFile())) {
                PDFTextStripper stripper = new PDFTextStripper();
                extractedText = stripper.getText(document);
            } catch (IOException e) {
                Files.deleteIfExists(targetPath);
                log.error("Failed to extract text from PDF for user {}", user.getEmail(), e);
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Failed to extract text from PDF: " + e.getMessage(), e);
            }

            Resume resume = Resume.builder()
                    .user(user)
                    .fileName(uniqueFileName)
                    .filePath(targetPath.toString())
                    .fileSize(file.getSize())
                    .mimeType(contentType)
                    .extractedText(extractedText)
                    .processingStatus(ProcessingStatus.TEXT_EXTRACTED)
                    .embeddingGenerated(false)
                    .uploadedAt(LocalDateTime.now())
                    .build();

            resume = resumeRepository.save(resume);

            ResumeResponse response = ResumeResponse.builder()
                    .resumeId(resume.getResumeId())
                    .userId(user.getUserId())
                    .fileName(resume.getFileName())
                    .filePath(resume.getFilePath())
                    .fileSize(resume.getFileSize())
                    .mimeType(resume.getMimeType())
                    .uploadedAt(resume.getUploadedAt())
                    .processingStatus(resume.getProcessingStatus())
                    .embeddingGenerated(resume.getEmbeddingGenerated())
                    .build();

            log.info("Resume uploaded and extracted successfully for user {}: {}", user.getEmail(), uniqueFileName);
            return new ApiResponse<>(true, "Resume uploaded and text extracted successfully", response);

        } catch (IOException e) {
            log.error("Failed to store file for user {}", user.getEmail(), e);
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Failed to store file: " + e.getMessage(), e);
        }
    }

    public ApiResponse<ResumeResponse> getMyResume(User user) {
        java.util.List<Resume> resumes = resumeRepository.findByUser(user);
        if (resumes.isEmpty()) {
            return new ApiResponse<>(false, "No resume uploaded yet", null);
        }
        Resume resume = resumes.get(resumes.size() - 1);
        ResumeResponse response = ResumeResponse.builder()
                .resumeId(resume.getResumeId())
                .userId(user.getUserId())
                .fileName(resume.getFileName())
                .filePath(resume.getFilePath())
                .fileSize(resume.getFileSize())
                .mimeType(resume.getMimeType())
                .uploadedAt(resume.getUploadedAt())
                .processingStatus(resume.getProcessingStatus())
                .embeddingGenerated(resume.getEmbeddingGenerated())
                .build();
        return new ApiResponse<>(true, "Resume retrieved successfully", response);
    }
}
