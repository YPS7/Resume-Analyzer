package com.yashresumeanalyzer.resumebackend.controller;

import com.yashresumeanalyzer.resumebackend.dto.JobDescriptionDTO;
import com.yashresumeanalyzer.resumebackend.service.JobDescriptionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/job-descriptions")
@CrossOrigin(origins = "http://localhost:3000") // Allow frontend access
@RequiredArgsConstructor
public class JobDescriptionController {

    private final JobDescriptionService jobDescriptionService;

    // POST /api/job-descriptions
    @PostMapping
    public ResponseEntity<JobDescriptionDTO> createJobDescription(@RequestBody JobDescriptionDTO jdDTO) {
        JobDescriptionDTO savedJD = jobDescriptionService.saveJobDescription(
                jdDTO.getContentText(),
                jdDTO.getTitle(),
                jdDTO.getChecksum());
        return ResponseEntity.ok(savedJD);
    }

    // GET /api/job-descriptions
    @GetMapping
    public ResponseEntity<List<JobDescriptionDTO>> getAllJobDescriptions() {
        return ResponseEntity.ok(jobDescriptionService.getAllJobDescriptions());
    }
}
