package com.internmatch.backend.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class InternshipRequest {

    @NotBlank
    private String title;

    @NotBlank
    private String company;

    @NotBlank
    private String location;

    private String description;

    private String requiredSkills;

    private String stipend;

    private String duration;

    private String mode;

    private String eligibility;

    private String applyUrl;
}