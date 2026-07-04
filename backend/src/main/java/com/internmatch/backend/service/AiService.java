package com.internmatch.backend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.time.Duration;
import java.util.Map;

@Service
public class AiService {

    private final RestClient restClient;

    public AiService(
            @Value("${ai.service.url}") String aiServiceUrl
    ) {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout((int) Duration.ofSeconds(5).toMillis());
        factory.setReadTimeout((int) Duration.ofSeconds(10).toMillis());

        this.restClient = RestClient.builder()
                .baseUrl(aiServiceUrl)
                .requestFactory(factory)
                .build();
    }

    public boolean checkHealth() {
        try {
            Map<?, ?> response = restClient.get()
                    .uri("/health")
                    .retrieve()
                    .body(Map.class);
            if (response != null) {
                return "healthy".equals(response.get("status"));
            }
            return false;
        } catch (Exception e) {
            System.err.println("AI Service Health Check Failed: " + e.getMessage());
            return false;
        }
    }

    public Map<?, ?> generateRecommendations(String resumeText, java.util.List<Map<String, Object>> internships) {
        return restClient.post()
                .uri("/recommendations/generate")
                .body(Map.of(
                        "resume_text", resumeText,
                        "internships", internships
                ))
                .retrieve()
                .body(Map.class);
    }
}
