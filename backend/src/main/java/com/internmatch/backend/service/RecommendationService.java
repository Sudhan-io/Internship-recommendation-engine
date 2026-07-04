package com.internmatch.backend.service;

import com.internmatch.backend.dto.ApiResponse;
import com.internmatch.backend.entity.*;
import com.internmatch.backend.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.util.*;

import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class RecommendationService {

    private final ResumeRepository resumeRepository;
    private final InternshipRepository internshipRepository;
    private final RecommendationBatchRepository batchRepository;
    private final RecommendationRepository recommendationRepository;
    private final AiService aiService;

    @Transactional
    public ApiResponse<Object> getRecommendations(Authentication authentication) {
        User user = (User) authentication.getPrincipal();
        List<Resume> resumes = resumeRepository.findByUser(user);
        if (resumes.isEmpty()) {
            log.warn("Cache fetch failed: User {} has no resume", user.getEmail());
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Please upload your resume first to get recommendations");
        }
        Resume resume = resumes.get(resumes.size() - 1);

        List<RecommendationBatch> batches = batchRepository.findByResumeOrderByGeneratedAtDesc(resume);
        if (!batches.isEmpty() && resume.getProcessingStatus() == ProcessingStatus.RECOMMENDATION_READY) {
            RecommendationBatch latestBatch = batches.get(0);
            List<Recommendation> storedRecs = recommendationRepository.findByBatch(latestBatch);
            
            storedRecs.sort((r1, r2) -> Double.compare(r2.getFinalScore(), r1.getFinalScore()));
            
            log.info("Recommendations retrieved from cache successfully for user {} (batchId={})", user.getEmail(), latestBatch.getBatchId());
            List<Map<String, Object>> mappedResults = mapRecommendationsToResponse(storedRecs);
            return new ApiResponse<>(true, "Recommendations retrieved from cache successfully", mappedResults);
        }

        log.info("No cached recommendations or resume status not ready for user {}. Triggering generation.", user.getEmail());
        return generateRecommendations(authentication);
    }

    @Transactional
    public ApiResponse<Object> generateRecommendations(Authentication authentication) {
        User user = (User) authentication.getPrincipal();
        List<Resume> resumes = resumeRepository.findByUser(user);
        if (resumes.isEmpty()) {
            log.warn("Generation failed: User {} has no resume", user.getEmail());
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Please upload your resume first to get recommendations");
        }
        Resume resume = resumes.get(resumes.size() - 1);

        log.info("Generating recommendations for user {}, resumeId={}", user.getEmail(), resume.getResumeId());

        List<Internship> internships = internshipRepository.findAll();
        if (internships.isEmpty()) {
            log.warn("Generation failed: No internships in database");
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No internships found in the database. Please run dataset import first.");
        }

        List<Map<String, Object>> mappedInternships = new ArrayList<>();
        for (Internship intern : internships) {
            Map<String, Object> map = new HashMap<>();
            map.put("internship_id", intern.getInternshipId());
            map.put("title", intern.getTitle());
            map.put("company", intern.getCompany());
            map.put("location", intern.getLocation());
            map.put("mode", intern.getMode());
            map.put("duration", intern.getDuration());
            map.put("stipend", intern.getStipend());
            map.put("description", intern.getDescription());
            map.put("eligibility", intern.getEligibility());
            map.put("apply_url", intern.getApplyUrl());
            map.put("required_skills", intern.getRequiredSkills());
            mappedInternships.add(map);
        }

        Map<?, ?> aiResponse;
        try {
            aiResponse = aiService.generateRecommendations(resume.getExtractedText(), mappedInternships);
        } catch (Exception e) {
            log.error("AI service failure while generating recommendations for user {}: {}", user.getEmail(), e.getMessage(), e);
            throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE, "AI Service is currently unavailable: " + e.getMessage(), e);
        }

        if (aiResponse == null || !"success".equals(aiResponse.get("status"))) {
            log.error("AI service returned unsuccessful response status for user {}", user.getEmail());
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "AI Service failed to generate recommendations");
        }

        String modelName = (String) aiResponse.get("model_name");
        List<?> rawRecs = (List<?>) aiResponse.get("recommendations");
        if (rawRecs == null) {
            rawRecs = new ArrayList<>();
        }

        RecommendationBatch batch = RecommendationBatch.builder()
                .user(user)
                .resume(resume)
                .modelName(modelName != null ? modelName : "all-MiniLM-L6-v2")
                .recommendationCount(rawRecs.size())
                .generatedAt(java.time.LocalDateTime.now())
                .build();
        batch = batchRepository.save(batch);
        log.info("Persisted new RecommendationBatch (batchId={}) with {} recommendations for user {}", batch.getBatchId(), batch.getRecommendationCount(), user.getEmail());

        List<Recommendation> savedRecs = new ArrayList<>();
        for (Object obj : rawRecs) {
            if (obj instanceof Map) {
                Map<?, ?> recMap = (Map<?, ?>) obj;
                
                Number internshipIdNum = (Number) recMap.get("internship_id");
                if (internshipIdNum == null) continue;
                Long internshipId = internshipIdNum.longValue();
                
                Internship internship = internshipRepository.findById(internshipId)
                        .orElseThrow(() -> new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Invalid internship ID returned by AI Service: " + internshipId));

                Number finalScore = (Number) recMap.get("final_score");
                
                Map<?, ?> breakdown = (Map<?, ?>) recMap.get("score_breakdown");
                Number semScore = breakdown != null ? (Number) breakdown.get("semantic_similarity") : 0.0;
                Number skillScore = breakdown != null ? (Number) breakdown.get("skill_match") : 0.0;
                Number eduScore = breakdown != null ? (Number) breakdown.get("education_match") : 0.0;
                Number expScore = breakdown != null ? (Number) breakdown.get("experience_match") : 0.0;
                Number eligScore = breakdown != null ? (Number) breakdown.get("eligibility_match") : 0.0;

                String explanationText = (String) recMap.get("explanation_text");
                
                List<?> matchedSkillsList = (List<?>) recMap.get("matched_skills");
                String matchedSkills = matchedSkillsList != null ? String.join(", ", (List<String>) matchedSkillsList) : "";
                
                List<?> missingSkillsList = (List<?>) recMap.get("missing_skills");
                String missingSkills = missingSkillsList != null ? String.join(", ", (List<String>) missingSkillsList) : "";

                Recommendation rec = Recommendation.builder()
                        .batch(batch)
                        .user(user)
                        .internship(internship)
                        .finalScore(finalScore != null ? finalScore.doubleValue() : 0.0)
                        .semanticScore(semScore != null ? semScore.doubleValue() : 0.0)
                        .skillScore(skillScore != null ? skillScore.doubleValue() : 0.0)
                        .educationScore(eduScore != null ? eduScore.doubleValue() : 0.0)
                        .experienceScore(expScore != null ? expScore.doubleValue() : 0.0)
                        .eligibilityScore(eligScore != null ? eligScore.doubleValue() : 0.0)
                        .explanationText(explanationText)
                        .matchedSkills(matchedSkills)
                        .missingSkills(missingSkills)
                        .build();
                
                savedRecs.add(recommendationRepository.save(rec));
            }
        }

        resume.setProcessingStatus(ProcessingStatus.RECOMMENDATION_READY);
        resume.setEmbeddingGenerated(true);
        resumeRepository.save(resume);

        savedRecs.sort((r1, r2) -> Double.compare(r2.getFinalScore(), r1.getFinalScore()));

        List<Map<String, Object>> mappedResults = mapRecommendationsToResponse(savedRecs);
        return new ApiResponse<>(true, "Recommendations generated successfully", mappedResults);
    }

    private List<Map<String, Object>> mapRecommendationsToResponse(List<Recommendation> recs) {
        List<Map<String, Object>> list = new ArrayList<>();
        for (Recommendation rec : recs) {
            Map<String, Object> map = new HashMap<>();
            map.put("internship_id", rec.getInternship().getInternshipId());
            map.put("title", rec.getInternship().getTitle());
            map.put("company", rec.getInternship().getCompany());
            map.put("location", rec.getInternship().getLocation());
            map.put("mode", rec.getInternship().getMode());
            map.put("description", rec.getInternship().getDescription());
            map.put("required_skills", rec.getInternship().getRequiredSkills());
            map.put("stipend", rec.getInternship().getStipend());
            map.put("duration", rec.getInternship().getDuration());
            map.put("eligibility", rec.getInternship().getEligibility());
            map.put("apply_url", rec.getInternship().getApplyUrl());
            map.put("final_score", rec.getFinalScore());
            
            Map<String, Object> breakdown = new HashMap<>();
            breakdown.put("semantic_similarity", rec.getSemanticScore());
            breakdown.put("skill_match", rec.getSkillScore());
            breakdown.put("education_match", rec.getEducationScore());
            breakdown.put("experience_match", rec.getExperienceScore());
            breakdown.put("eligibility_match", rec.getEligibilityScore());
            map.put("score_breakdown", breakdown);
            
            List<String> matched = rec.getMatchedSkills() != null && !rec.getMatchedSkills().isEmpty() 
                    ? Arrays.asList(rec.getMatchedSkills().split(",\\s*")) 
                    : new ArrayList<>();
            List<String> missing = rec.getMissingSkills() != null && !rec.getMissingSkills().isEmpty() 
                    ? Arrays.asList(rec.getMissingSkills().split(",\\s*")) 
                    : new ArrayList<>();
            
            map.put("matched_skills", matched);
            map.put("missing_skills", missing);
            map.put("matched_education", new ArrayList<>());
            map.put("missing_education", new ArrayList<>());
            map.put("matched_experience", new ArrayList<>());
            map.put("eligibility_status", rec.getEligibilityScore() > 0.0);
            map.put("explanation_text", rec.getExplanationText());
            list.add(map);
        }
        return list;
    }
}
