package com.internmatch.backend.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class StudentProfileRequest {

    @NotBlank(message = "College name is required")
    private String collegeName;

    @NotBlank(message = "Department is required")
    private String department;

    @NotNull(message = "Year of study is required")
    @Min(value = 1, message = "Year of study must be at least 1")
    @Max(value = 5, message = "Year of study must be at most 5")
    private Integer yearOfStudy;

    @NotNull(message = "CGPA is required")
    @DecimalMin(value = "0.0", message = "CGPA must be at least 0.0")
    @DecimalMax(value = "10.0", message = "CGPA must be at most 10.0")
    private Double cgpa;

    @NotBlank(message = "Phone number is required")
    @Pattern(regexp = "^[0-9]{10,15}$", message = "Phone number must be between 10 and 15 digits")
    private String phone;

    private String linkedinUrl;

    private String githubUrl;
}