package com.internmatch.backend.repository;

import com.internmatch.backend.entity.StudentProfile;
import com.internmatch.backend.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface StudentProfileRepository extends JpaRepository<StudentProfile, Long> {

    Optional<StudentProfile> findByUser(User user);

}