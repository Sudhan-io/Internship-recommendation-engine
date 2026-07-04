package com.internmatch.backend.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "internships")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Internship {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long internshipId;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String company;

    @Column(nullable = false)
    private String location;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String requiredSkills;

    private String stipend;

    private String duration;

    private String mode; // Remote / Hybrid / On-site

    private String eligibility;

    private String applyUrl;
}