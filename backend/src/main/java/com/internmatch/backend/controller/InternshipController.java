package com.internmatch.backend.controller;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.InternshipRequest;
import com.internmatch.backend.dto.InternshipResponse;
import com.internmatch.backend.service.InternshipService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/internships")
@RequiredArgsConstructor
public class InternshipController {

    private final InternshipService internshipService;

    @PostMapping
    public ApiResponse<InternshipResponse> createInternship(
            @Valid @RequestBody InternshipRequest request) {

        return internshipService.createInternship(request);
    }

    @GetMapping
    public ApiResponse<List<InternshipResponse>> getAllInternships() {
        return internshipService.getAllInternships();
    }

    @GetMapping("/{id}")
    public ApiResponse<InternshipResponse> getInternshipById(
            @PathVariable Long id) {

        return internshipService.getInternshipById(id);
    }

    @PutMapping("/{id}")
    public ApiResponse<InternshipResponse> updateInternship(
            @PathVariable Long id,
            @Valid @RequestBody InternshipRequest request) {

        return internshipService.updateInternship(id, request);
    }

    @DeleteMapping("/{id}")
    public ApiResponse<String> deleteInternship(
            @PathVariable Long id) {

        return internshipService.deleteInternship(id);
    }
}