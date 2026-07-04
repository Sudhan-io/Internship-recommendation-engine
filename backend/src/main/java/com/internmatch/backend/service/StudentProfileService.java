package com.internmatch.backend.service;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.StudentProfileRequest;
import com.internmatch.backend.dto.StudentProfileResponse;
import com.internmatch.backend.entity.StudentProfile;
import com.internmatch.backend.entity.User;
import com.internmatch.backend.repository.StudentProfileRepository;
//import com.internmatch.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class StudentProfileService {

    private final StudentProfileRepository profileRepository;
    //private final UserRepository userRepository;

    public ApiResponse<StudentProfileResponse> createProfile(
            StudentProfileRequest request,
            Authentication authentication
    ) {

        User user = (User) authentication.getPrincipal();

        if (profileRepository.findByUser(user).isPresent()) {
            throw new RuntimeException("Profile already exists");
        }

        StudentProfile profile = StudentProfile.builder()
                .user(user)
                .collegeName(request.getCollegeName())
                .department(request.getDepartment())
                .yearOfStudy(request.getYearOfStudy())
                .cgpa(request.getCgpa())
                .phone(request.getPhone())
                .linkedinUrl(request.getLinkedinUrl())
                .githubUrl(request.getGithubUrl())
                .build();

        profileRepository.save(profile);

        StudentProfileResponse response = StudentProfileResponse.builder()
                .profileId(profile.getProfileId())
                .collegeName(profile.getCollegeName())
                .department(profile.getDepartment())
                .yearOfStudy(profile.getYearOfStudy())
                .cgpa(profile.getCgpa())
                .phone(profile.getPhone())
                .linkedinUrl(profile.getLinkedinUrl())
                .githubUrl(profile.getGithubUrl())
                .build();

        return new ApiResponse<>(
                true,
                "Profile Created Successfully",
                response
        );
    }

    public ApiResponse<StudentProfileResponse> getProfile(Authentication authentication) {
        User user = (User) authentication.getPrincipal();
        return profileRepository.findByUser(user)
                .map(profile -> new ApiResponse<>(true, "Profile retrieved successfully", 
                        StudentProfileResponse.builder()
                                .profileId(profile.getProfileId())
                                .collegeName(profile.getCollegeName())
                                .department(profile.getDepartment())
                                .yearOfStudy(profile.getYearOfStudy())
                                .cgpa(profile.getCgpa())
                                .phone(profile.getPhone())
                                .linkedinUrl(profile.getLinkedinUrl())
                                .githubUrl(profile.getGithubUrl())
                                .build()))
                .orElse(new ApiResponse<>(false, "Profile not found", null));
    }

    public ApiResponse<StudentProfileResponse> updateProfile(
            StudentProfileRequest request,
            Authentication authentication
    ) {
        User user = (User) authentication.getPrincipal();
        StudentProfile profile = profileRepository.findByUser(user)
                .orElseThrow(() -> new RuntimeException("Profile not found"));
                
        profile.setCollegeName(request.getCollegeName());
        profile.setDepartment(request.getDepartment());
        profile.setYearOfStudy(request.getYearOfStudy());
        profile.setCgpa(request.getCgpa());
        profile.setPhone(request.getPhone());
        profile.setLinkedinUrl(request.getLinkedinUrl());
        profile.setGithubUrl(request.getGithubUrl());
        
        profileRepository.save(profile);
        
        StudentProfileResponse response = StudentProfileResponse.builder()
                .profileId(profile.getProfileId())
                .collegeName(profile.getCollegeName())
                .department(profile.getDepartment())
                .yearOfStudy(profile.getYearOfStudy())
                .cgpa(profile.getCgpa())
                .phone(profile.getPhone())
                .linkedinUrl(profile.getLinkedinUrl())
                .githubUrl(profile.getGithubUrl())
                .build();
                
        return new ApiResponse<>(true, "Profile Updated Successfully", response);
    }
}