package com.internmatch.backend.repository;

import com.internmatch.backend.entity.Internship;
import org.springframework.data.jpa.repository.JpaRepository;

public interface InternshipRepository extends JpaRepository<Internship, Long> {
}