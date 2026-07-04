package com.internmatch.backend.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class InternshipResponse {

    private Long internshipId;

    private String title;

    private String company;

    private String location;

    private String description;

    private String requiredSkills;

    private String stipend;

    private String duration;

    private String mode;

    private String eligibility;

    private String applyUrl;
}