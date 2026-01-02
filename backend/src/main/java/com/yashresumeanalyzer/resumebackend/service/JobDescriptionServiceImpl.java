package com.yashresumeanalyzer.resumebackend.service;

import com.yashresumeanalyzer.resumebackend.dto.JobDescriptionDTO;
import com.yashresumeanalyzer.resumebackend.entity.JobDescription;
import com.yashresumeanalyzer.resumebackend.repository.JobDescriptionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class JobDescriptionServiceImpl implements JobDescriptionService {

    private final JobDescriptionRepository jobDescriptionRepository;

    @Override
    public JobDescriptionDTO saveJobDescription(String content, String title, String checksum) {
        // 1. Check for duplicate
        Optional<JobDescription> existing = jobDescriptionRepository.findByChecksum(checksum);
        if (existing.isPresent()) {
            return mapToDTO(existing.get());
        }

        // 2. Save new
        JobDescription jd = new JobDescription();
        jd.setContentText(content);
        jd.setTitle(title);
        jd.setChecksum(checksum);

        JobDescription savedJd = jobDescriptionRepository.save(jd);
        return mapToDTO(savedJd);
    }

    @Override
    public List<JobDescriptionDTO> getAllJobDescriptions() {
        return jobDescriptionRepository.findAll().stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Optional<JobDescriptionDTO> getJobDescriptionById(Long id) {
        return jobDescriptionRepository.findById(id).map(this::mapToDTO);
    }

    private JobDescriptionDTO mapToDTO(JobDescription jd) {
        JobDescriptionDTO dto = new JobDescriptionDTO();
        dto.setId(jd.getId());
        dto.setTitle(jd.getTitle());
        dto.setContentText(jd.getContentText());
        dto.setChecksum(jd.getChecksum());
        dto.setCreatedAt(jd.getCreatedAt());
        return dto;
    }
}
