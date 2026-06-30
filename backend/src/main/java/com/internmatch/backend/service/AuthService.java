package com.internmatch.backend.service;
import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.dto.RegisterRequest;
import com.internmatch.backend.entity.Role;
import com.internmatch.backend.entity.User;
import com.internmatch.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import com.internmatch.backend.dto.LoginRequest;
import java.util.Optional;
import com.internmatch.backend.security.JwtService;
import com.internmatch.backend.dto.AuthResponse;


@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

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
    public ApiResponse<Object> login(LoginRequest request) {

    Optional<User> optionalUser = userRepository.findByEmail(request.getEmail());

    if (optionalUser.isEmpty()) {
        return new ApiResponse<>(
                false,
                "Invalid Email or Password",
                null
        );
    }

    User user = optionalUser.get();

    if (!passwordEncoder.matches(
            request.getPassword(),
            user.getPasswordHash()
    )) {

        return new ApiResponse<>(
                false,
                "Invalid Email or Password",
                null
        );
    }

    String token = jwtService.generateToken(user);

AuthResponse response = new AuthResponse(
        token,
        user.getEmail(),
        user.getRole().name()
);

return new ApiResponse<>(
        true,
        "Login Successful",
        response
);
}
}