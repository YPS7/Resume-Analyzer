package com.yashresumeanalyzer.resumebackend.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "match_results")
@Data
public class MatchResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Links to the Resume Table
    @ManyToOne
    @JoinColumn(name = "resume_id", nullable = false)
    private Resume resume;

    // Links to the JD Table
    @ManyToOne
    @JoinColumn(name = "job_description_id", nullable = false)
    private JobDescription jobDescription;

    // AI Analysis Data
    private Double score;
    private String verdict;

    @Column(columnDefinition = "TEXT")
    private String missingSkills;

    @Column(columnDefinition = "TEXT")
    private String summary;

    private Boolean dealbreaker;

    @Column(updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}