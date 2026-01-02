package com.yashresumeanalyzer.resumebackend.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "resumes")
@Data
public class Resume {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Stores the raw text extracted from the PDF
    @Column(columnDefinition = "TEXT", nullable = false)
    private String contentText;

    // "PDF" or "WEBSITE"
    private String sourceType;

    // Unique hash to prevent duplicate uploads
    @Column(unique = true)
    private String checksum;

    @Column(updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}