package com.yashresumeanalyzer.resumebackend.controller;

import com.yashresumeanalyzer.resumebackend.dto.MatchResultDTO;
import com.yashresumeanalyzer.resumebackend.service.AnalysisService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/analyze")
@CrossOrigin(origins = "http://localhost:3000")
@RequiredArgsConstructor
public class AnalysisController {

    private final AnalysisService analysisService;

    // POST /api/analyze?resumeId=1&jdId=2
    @PostMapping
    public ResponseEntity<MatchResultDTO> analyzeResume(
            @RequestParam Long resumeId,
            @RequestParam Long jdId) {

        MatchResultDTO result = analysisService.analyzeResume(resumeId, jdId);
        return ResponseEntity.ok(result);
    }
}
