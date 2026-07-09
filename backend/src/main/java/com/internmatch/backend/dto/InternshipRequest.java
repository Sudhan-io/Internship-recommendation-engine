package com.internmatch.backend.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class InternshipRequest {

    @NotBlank(message = "Title is required")
    private String title;

    @NotBlank(message = "Company is required")
    private String company;

    @NotBlank(message = "Location is required")
    private String location;

    private String description;

    private String requiredSkills;

    private String stipend;

    private String duration;

    private String mode;

    private String eligibility;

    private String applyUrl;
}