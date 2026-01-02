package com.yashresumeanalyzer.resumebackend.service;

import com.yashresumeanalyzer.resumebackend.dto.ResumeDTO;
import com.yashresumeanalyzer.resumebackend.entity.Resume;
import com.yashresumeanalyzer.resumebackend.repository.ResumeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ResumeServiceImpl implements ResumeService {

    private final ResumeRepository resumeRepository;

    @Override
    public ResumeDTO saveResume(String content, String sourceType, String checksum) {
        // 1. Check for duplicate using hash
        Optional<Resume> existing = resumeRepository.findByChecksum(checksum);
        if (existing.isPresent()) {
            return mapToDTO(existing.get());
        }

        // 2. Create and Save new Resume
        Resume resume = new Resume();
        resume.setContentText(content);
        resume.setSourceType(sourceType);
        resume.setChecksum(checksum);

        Resume savedResume = resumeRepository.save(resume);
        return mapToDTO(savedResume);
    }

    @Override
    public List<ResumeDTO> getAllResumes() {
        return resumeRepository.findAll().stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Optional<ResumeDTO> getResumeById(Long id) {
        return resumeRepository.findById(id).map(this::mapToDTO);
    }

    // Helper method to convert Entity -> DTO
    private ResumeDTO mapToDTO(Resume resume) {
        ResumeDTO dto = new ResumeDTO();
        dto.setId(resume.getId());
        dto.setContentText(resume.getContentText());
        dto.setSourceType(resume.getSourceType());
        dto.setChecksum(resume.getChecksum());
        dto.setCreatedAt(resume.getCreatedAt());
        return dto;
    }
}
