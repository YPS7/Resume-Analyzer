package com.yashresumeanalyzer.resumebackend.repository;

import com.yashresumeanalyzer.resumebackend.entity.JobDescription;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface JobDescriptionRepository extends JpaRepository<JobDescription, Long> {
    Optional<JobDescription> findByChecksum(String checksum);
}