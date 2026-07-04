package com.internmatch.backend.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "student_profiles")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StudentProfile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long profileId;

    @OneToOne
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private User user;

    @Column(nullable = false)
    private String collegeName;

    @Column(nullable = false)
    private String department;

    @Column(nullable = false)
    private Integer yearOfStudy;

    private Double cgpa;

    private String phone;

    private String linkedinUrl;

    private String githubUrl;
}