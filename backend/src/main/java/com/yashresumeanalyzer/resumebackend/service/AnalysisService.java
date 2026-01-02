package com.yashresumeanalyzer.resumebackend.service;

import com.yashresumeanalyzer.resumebackend.dto.MatchResultDTO;

public interface AnalysisService {
    MatchResultDTO analyzeResume(Long resumeId, Long jobDescriptionId);
}
