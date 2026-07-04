package com.internmatch.backend.controller;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.StudentProfileRequest;
import com.internmatch.backend.dto.StudentProfileResponse;
import com.internmatch.backend.service.StudentProfileService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/student")
@RequiredArgsConstructor
public class StudentProfileController {

    private final StudentProfileService studentProfileService;

    @PostMapping("/profile")
    public ApiResponse<StudentProfileResponse> createProfile(
            @Valid @RequestBody StudentProfileRequest request,
            Authentication authentication
    ) {
        return studentProfileService.createProfile(request, authentication);
    }

    @GetMapping("/profile")
    public ApiResponse<StudentProfileResponse> getProfile(
            Authentication authentication
    ) {
        return studentProfileService.getProfile(authentication);
    }

    @PutMapping("/profile")
    public ApiResponse<StudentProfileResponse> updateProfile(
            @Valid @RequestBody StudentProfileRequest request,
            Authentication authentication
    ) {
        return studentProfileService.updateProfile(request, authentication);
    }
}