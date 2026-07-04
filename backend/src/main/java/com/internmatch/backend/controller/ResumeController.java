package com.internmatch.backend.controller;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.ResumeResponse;
import com.internmatch.backend.entity.User;
import com.internmatch.backend.service.ResumeService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/resumes")
@RequiredArgsConstructor
public class ResumeController {

    private final ResumeService resumeService;

    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ApiResponse<ResumeResponse> uploadResume(
            @RequestParam("file") MultipartFile file,
            Authentication authentication
    ) {
        User user = (User) authentication.getPrincipal();
        return resumeService.uploadAndExtractResume(file, user);
    }

    @GetMapping("/my-resume")
    public ApiResponse<ResumeResponse> getMyResume(
            Authentication authentication
    ) {
        User user = (User) authentication.getPrincipal();
        return resumeService.getMyResume(user);
    }
}
