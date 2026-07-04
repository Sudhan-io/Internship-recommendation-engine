package com.internmatch.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@AllArgsConstructor
public class StudentProfileResponse {

    private Long profileId;

    private String collegeName;

    private String department;

    private Integer yearOfStudy;

    private Double cgpa;

    private String phone;

    private String linkedinUrl;

    private String githubUrl;
}