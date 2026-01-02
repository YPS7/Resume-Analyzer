package com.yashresumeanalyzer.resumebackend.service;

import com.yashresumeanalyzer.resumebackend.dto.ResumeDTO;
import java.util.List;
import java.util.Optional;

public interface ResumeService {
    ResumeDTO saveResume(String content, String sourceType, String checksum);

    List<ResumeDTO> getAllResumes();

    Optional<ResumeDTO> getResumeById(Long id);
}
