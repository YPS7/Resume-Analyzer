package com.yashresumeanalyzer.resumebackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MatchResultDTO {
    private Long id;
    private Long resumeId;
    private Long jobDescriptionId;
    private Double score;
    private String verdict;
    private String missingSkills;
    private String summary;
    private Boolean dealbreaker;
    private LocalDateTime createdAt;
}
