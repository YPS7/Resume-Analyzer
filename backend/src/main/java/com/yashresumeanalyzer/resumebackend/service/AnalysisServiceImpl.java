package com.yashresumeanalyzer.resumebackend.service;

import com.yashresumeanalyzer.resumebackend.dto.MatchResultDTO;
import com.yashresumeanalyzer.resumebackend.entity.JobDescription;
import com.yashresumeanalyzer.resumebackend.entity.MatchResult;
import com.yashresumeanalyzer.resumebackend.entity.Resume;
import com.yashresumeanalyzer.resumebackend.repository.JobDescriptionRepository;
import com.yashresumeanalyzer.resumebackend.repository.MatchResultRepository;
import com.yashresumeanalyzer.resumebackend.repository.ResumeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.HttpClientErrorException;
import com.fasterxml.jackson.databind.ObjectMapper;

@Service
@RequiredArgsConstructor
public class AnalysisServiceImpl implements AnalysisService {

        private final ResumeRepository resumeRepository;
        private final JobDescriptionRepository jobDescriptionRepository;
        private final MatchResultRepository matchResultRepository;

        @Value("${spring.ai-engine.url}")
        private String aiEngineUrl;

        private final RestTemplate restTemplate = new RestTemplate();

        @Override
        public MatchResultDTO analyzeResume(Long resumeId, Long jobDescriptionId) {
                // 1. Fetch Entities
                Resume resume = resumeRepository.findById(resumeId)
                                .orElseThrow(() -> new RuntimeException("Resume not found"));
                JobDescription jd = jobDescriptionRepository.findById(jobDescriptionId)
                                .orElseThrow(() -> new RuntimeException("Job Description not found"));

                // 2. Prepare Request to AI Engine
                String apiUrl = aiEngineUrl + "/analyze";

                HttpHeaders headers = new HttpHeaders();
                headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

                MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
                map.add("jd_text", jd.getContentText());
                map.add("resume_text_raw", resume.getContentText());

                HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(map, headers);

                // 3. Call AI Engine
                MatchResult result = new MatchResult();
                result.setResume(resume);
                result.setJobDescription(jd);

                try {
                        ResponseEntity<Map> response = restTemplate.postForEntity(apiUrl, request, Map.class);

                        if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                                Map<String, Object> body = response.getBody();

                                Double score = Double.valueOf(body.get("score").toString());
                                String verdict = (String) body.get("verdict");
                                String summary = (String) body.get("summary");
                                Boolean dealbreaker = (Boolean) body.get("dealbreaker");
                                List<String> missingSkills = (List<String>) body.get("missing_skills");

                                result.setScore(score);
                                result.setVerdict(verdict);
                                result.setSummary(summary);
                                result.setDealbreaker(dealbreaker);
                                result.setMissingSkills(String.join(", ", missingSkills));
                        } else {
                                throw new RuntimeException(
                                                "AI Engine returned unexpected status: " + response.getStatusCode());
                        }
                } catch (HttpClientErrorException e) {
                        throw new RuntimeException("Error calling AI Engine: " + e.getResponseBodyAsString(), e);
                } catch (Exception e) {
                        throw new RuntimeException("Failed to analyze resume via AI Engine", e);
                }

                // 4. Save Result
                MatchResult savedResult = matchResultRepository.save(result);

                // 5. Return DTO
                return mapToDTO(savedResult);
        }

        private MatchResultDTO mapToDTO(MatchResult result) {
                MatchResultDTO dto = new MatchResultDTO();
                dto.setId(result.getId());
                dto.setResumeId(result.getResume().getId());
                dto.setJobDescriptionId(result.getJobDescription().getId());
                dto.setScore(result.getScore());
                dto.setVerdict(result.getVerdict());
                dto.setMissingSkills(result.getMissingSkills());
                dto.setSummary(result.getSummary());
                dto.setDealbreaker(result.getDealbreaker());
                dto.setCreatedAt(result.getCreatedAt());
                return dto;
        }
}
