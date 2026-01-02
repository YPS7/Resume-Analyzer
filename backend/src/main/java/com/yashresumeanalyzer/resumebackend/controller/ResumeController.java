package com.yashresumeanalyzer.resumebackend.controller;

import com.yashresumeanalyzer.resumebackend.dto.ResumeDTO;
import com.yashresumeanalyzer.resumebackend.service.ResumeService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/resumes")
@CrossOrigin(origins = "http://localhost:3000") // Allow frontend access
@RequiredArgsConstructor
public class ResumeController {

    private final ResumeService resumeService;

    // POST /api/resumes
    // Simple text upload for now. Accepts JSON: { "contentText": "...", "checksum":
    // "...", "sourceType": "..." }
    @PostMapping
    public ResponseEntity<ResumeDTO> createResume(@RequestBody ResumeDTO resumeDTO) {
        ResumeDTO savedResume = resumeService.saveResume(
                resumeDTO.getContentText(),
                resumeDTO.getSourceType(),
                resumeDTO.getChecksum());
        return ResponseEntity.ok(savedResume);
    }

    // GET /api/resumes
    @GetMapping
    public ResponseEntity<List<ResumeDTO>> getAllResumes() {
        return ResponseEntity.ok(resumeService.getAllResumes());
    }
}
