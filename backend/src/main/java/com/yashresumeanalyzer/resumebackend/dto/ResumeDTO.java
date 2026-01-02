package com.yashresumeanalyzer.resumebackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ResumeDTO {
    private Long id;
    private String contentText;
    private String sourceType;
    private String checksum;
    private LocalDateTime createdAt;
}
