package com.yashresumeanalyzer.resumebackend.service;

import com.yashresumeanalyzer.resumebackend.dto.JobDescriptionDTO;
import java.util.List;
import java.util.Optional;

public interface JobDescriptionService {
    JobDescriptionDTO saveJobDescription(String content, String title, String checksum);

    List<JobDescriptionDTO> getAllJobDescriptions();

    Optional<JobDescriptionDTO> getJobDescriptionById(Long id);
}
