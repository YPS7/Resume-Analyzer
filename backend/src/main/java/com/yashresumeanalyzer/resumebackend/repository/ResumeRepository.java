package com.yashresumeanalyzer.resumebackend.repository;

import com.yashresumeanalyzer.resumebackend.entity.Resume;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface ResumeRepository extends JpaRepository<Resume, Long> {
    Optional<Resume> findByChecksum(String checksum);
}