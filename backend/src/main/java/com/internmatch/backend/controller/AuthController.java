package com.internmatch.backend.controller;
import jakarta.validation.Valid;
import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.RegisterRequest;
import com.internmatch.backend.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import com.internmatch.backend.dto.LoginRequest;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
   public ApiResponse<Object> register(
        @Valid @RequestBody RegisterRequest request) {
        return authService.register(request);
    }
    @GetMapping("/test")
public String test() {
    return "JWT Authentication Working";
}
    @PostMapping("/login")
public ApiResponse<Object> login(
        @Valid @RequestBody LoginRequest request
) {
    return authService.login(request);
}
}