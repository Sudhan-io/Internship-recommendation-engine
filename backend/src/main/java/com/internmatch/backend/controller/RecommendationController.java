package com.internmatch.backend.controller;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.service.RecommendationService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/recommendations")
@RequiredArgsConstructor
public class RecommendationController {

    private final RecommendationService recommendationService;

    @GetMapping
    public ApiResponse<Object> getRecommendations(Authentication authentication) {
        return recommendationService.getRecommendations(authentication);
    }

    @PostMapping("/generate")
    public ApiResponse<Object> generateRecommendations(Authentication authentication) {
        return recommendationService.generateRecommendations(authentication);
    }
}
