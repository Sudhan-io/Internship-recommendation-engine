package com.internmatch.backend.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StudentController {

    @GetMapping("/api/student/profile-dummy")
    public String profile() {
        return "Student Profile";
    }
}