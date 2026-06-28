package com.internmatch.backend.controller;

import com.internmatch.backend.dto.AuthResponse;
import com.internmatch.backend.dto.RegisterRequest;
import com.internmatch.backend.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    public AuthResponse register(@RequestBody RegisterRequest request) {
        return authService.register(request);
    }
}