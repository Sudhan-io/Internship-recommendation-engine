package com.internmatch.backend;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.ResumeResponse;
import com.internmatch.backend.entity.ProcessingStatus;
import com.internmatch.backend.entity.Role;
import com.internmatch.backend.entity.User;
import com.internmatch.backend.repository.UserRepository;
import com.internmatch.backend.repository.ResumeRepository;
import com.internmatch.backend.service.ResumeService;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.font.PDType1Font;
import org.apache.pdfbox.pdmodel.font.Standard14Fonts;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.transaction.annotation.Transactional;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@Transactional
class ResumeServiceTest {

    @Autowired
    private ResumeService resumeService;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ResumeRepository resumeRepository;

    private byte[] createTestPdf(String textContent) throws IOException {
        try (PDDocument doc = new PDDocument(); ByteArrayOutputStream baos = new ByteArrayOutputStream()) {
            PDPage page = new PDPage();
            doc.addPage(page);
            try (PDPageContentStream contentStream = new PDPageContentStream(doc, page)) {
                contentStream.beginText();
                contentStream.setFont(new PDType1Font(Standard14Fonts.FontName.HELVETICA), 12);
                contentStream.newLineAtOffset(100, 700);
                contentStream.showText(textContent);
                contentStream.endText();
            }
            doc.save(baos);
            return baos.toByteArray();
        }
    }

    @Test
    void testUploadAndExtractResumeSuccess() throws Exception {
        // Create user
        User user = User.builder()
                .fullName("Test Student")
                .email("student@test.com")
                .passwordHash("password")
                .role(Role.STUDENT)
                .build();
        user = userRepository.save(user);

        // Create mock PDF
        String sampleText = "This is a sample resume text with Python and Java skills.";
        byte[] pdfBytes = createTestPdf(sampleText);
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "test_resume.pdf",
                "application/pdf",
                pdfBytes
        );

        // Upload and extract
        ApiResponse<ResumeResponse> response = resumeService.uploadAndExtractResume(file, user);

        // Assertions
        assertTrue(response.isSuccess());
        assertNotNull(response.getData());
        ResumeResponse resumeResponse = response.getData();
        assertEquals(user.getUserId(), resumeResponse.getUserId());
        assertEquals("application/pdf", resumeResponse.getMimeType());
        assertEquals(ProcessingStatus.TEXT_EXTRACTED, resumeResponse.getProcessingStatus());
        assertFalse(resumeResponse.getEmbeddingGenerated());
        assertNotNull(resumeResponse.getFilePath());

        // Assert file exists on disk
        assertTrue(Files.exists(Paths.get(resumeResponse.getFilePath())));

        // Clean up file from disk after test
        Files.deleteIfExists(Paths.get(resumeResponse.getFilePath()));
    }
}
