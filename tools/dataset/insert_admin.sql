-- insert_admin.sql
-- Inserts a default admin user into the users table.
-- Passwords should be hashed using BCrypt if used by Spring Boot.
-- Assuming $2a$10$abcdefghijklmnopqrstuv is a dummy hash for 'admin123'

INSERT INTO users (full_name, email, password, role)
VALUES ('Admin User', 'admin@example.com', '$2a$10$abcdefghijklmnopqrstuv', 'ADMIN')
ON DUPLICATE KEY UPDATE email=email;
