package com.internmatch.backend.service;
import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.AuthResponse;
import com.internmatch.backend.dto.RegisterRequest;
import com.internmatch.backend.entity.Role;
import com.internmatch.backend.entity.User;
import com.internmatch.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public ApiResponse<Object> register(RegisterRequest request) {

        if (userRepository.existsByEmail(request.getEmail())) {
            return new ApiResponse<>(
        false,
        "Email already exists",
        null
);
        }

        User user = User.builder()
                .fullName(request.getFullName())
                .email(request.getEmail())
                .passwordHash(passwordEncoder.encode(request.getPassword()))
                .role(Role.STUDENT)
                .build();

        userRepository.save(user);

        return new ApiResponse<>(
        true,
        "Registration Successful",
        null
);
    }
}