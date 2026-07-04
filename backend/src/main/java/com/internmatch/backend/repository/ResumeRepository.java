package com.internmatch.backend.repository;

import com.internmatch.backend.entity.Resume;
import com.internmatch.backend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ResumeRepository extends JpaRepository<Resume, Long> {

    List<Resume> findByUser(User user);

}