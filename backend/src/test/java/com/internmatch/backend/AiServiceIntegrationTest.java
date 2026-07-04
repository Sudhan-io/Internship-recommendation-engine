package com.internmatch.backend;

import com.internmatch.backend.service.AiService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class AiServiceIntegrationTest {

    @Autowired
    private AiService aiService;

    @Test
    void testAiServiceHealthCheck() {
        boolean isHealthy = aiService.checkHealth();
        assertTrue(isHealthy, "FastAPI AI service should be running and healthy");
    }
}
