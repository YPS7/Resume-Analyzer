package com.yashresumeanalyzer.resumebackend.repository;

import com.yashresumeanalyzer.resumebackend.entity.MatchResult;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MatchResultRepository extends JpaRepository<MatchResult, Long> {
}