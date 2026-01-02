package com.yashresumeanalyzer.resumebackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class JobDescriptionDTO {
    private Long id;
    private String title;
    private String contentText;
    private String checksum;
    private LocalDateTime createdAt;
}
