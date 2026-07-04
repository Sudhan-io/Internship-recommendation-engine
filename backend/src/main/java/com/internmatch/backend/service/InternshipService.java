package com.internmatch.backend.service;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.InternshipRequest;
import com.internmatch.backend.dto.InternshipResponse;
import com.internmatch.backend.entity.Internship;
import com.internmatch.backend.repository.InternshipRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class InternshipService {

    private final InternshipRepository internshipRepository;

    public ApiResponse<InternshipResponse> createInternship(InternshipRequest request) {

        Internship internship = Internship.builder()
                .title(request.getTitle())
                .company(request.getCompany())
                .location(request.getLocation())
                .description(request.getDescription())
                .requiredSkills(request.getRequiredSkills())
                .stipend(request.getStipend())
                .duration(request.getDuration())
                .mode(request.getMode())
                .eligibility(request.getEligibility())
                .applyUrl(request.getApplyUrl())
                .build();

        internship = internshipRepository.save(internship);

        return new ApiResponse<>(
                true,
                "Internship Created Successfully",
                mapToResponse(internship)
        );
    }

    public ApiResponse<List<InternshipResponse>> getAllInternships() {

        List<InternshipResponse> internships = internshipRepository.findAll()
                .stream()
                .map(this::mapToResponse)
                .toList();

        return new ApiResponse<>(true, "Internships Retrieved", internships);
    }

    public ApiResponse<InternshipResponse> getInternshipById(Long id) {

        Internship internship = internshipRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Internship not found"));

        return new ApiResponse<>(
                true,
                "Internship Retrieved",
                mapToResponse(internship)
        );
    }

    public ApiResponse<InternshipResponse> updateInternship(Long id, InternshipRequest request) {

        Internship internship = internshipRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Internship not found"));

        internship.setTitle(request.getTitle());
        internship.setCompany(request.getCompany());
        internship.setLocation(request.getLocation());
        internship.setDescription(request.getDescription());
        internship.setRequiredSkills(request.getRequiredSkills());
        internship.setStipend(request.getStipend());
        internship.setDuration(request.getDuration());
        internship.setMode(request.getMode());
        internship.setEligibility(request.getEligibility());
        internship.setApplyUrl(request.getApplyUrl());

        internshipRepository.save(internship);

        return new ApiResponse<>(
                true,
                "Internship Updated Successfully",
                mapToResponse(internship)
        );
    }

    public ApiResponse<String> deleteInternship(Long id) {

        Internship internship = internshipRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Internship not found"));

        internshipRepository.delete(internship);

        return new ApiResponse<>(
                true,
                "Internship Deleted Successfully",
                "Deleted"
        );
    }

    private InternshipResponse mapToResponse(Internship internship) {

        return InternshipResponse.builder()
                .internshipId(internship.getInternshipId())
                .title(internship.getTitle())
                .company(internship.getCompany())
                .location(internship.getLocation())
                .description(internship.getDescription())
                .requiredSkills(internship.getRequiredSkills())
                .stipend(internship.getStipend())
                .duration(internship.getDuration())
                .mode(internship.getMode())
                .eligibility(internship.getEligibility())
                .applyUrl(internship.getApplyUrl())
                .build();
    }
}