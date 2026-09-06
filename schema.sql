-- ============================================
-- ArthaSetu Database Schema
-- AI Powered Local Skill Intelligence Platform
-- ============================================

CREATE DATABASE IF NOT EXISTS arthasetu_db;
USE arthasetu_db;

-- ============================================
-- USERS TABLE
-- Stores both clients and workers
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,           -- Hashed password (Werkzeug)
    role ENUM('client', 'worker') NOT NULL,   -- User type
    phone VARCHAR(15),
    city VARCHAR(100) DEFAULT 'Bhopal',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- WORKERS TABLE
-- Extended profile for workers
-- ============================================
CREATE TABLE IF NOT EXISTS workers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_category VARCHAR(100) NOT NULL,     -- e.g. Plumber, Electrician
    experience_years INT DEFAULT 0,
    address TEXT,
    description TEXT,                          -- Short bio / about
    availability ENUM('available', 'busy', 'offline') DEFAULT 'available',
    rating DECIMAL(3,2) DEFAULT 0.00,
    total_jobs INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- JOBS TABLE
-- Client job postings
-- ============================================
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    title VARCHAR(200),
    description TEXT NOT NULL,                -- Natural language requirement
    location VARCHAR(200),
    status ENUM('open', 'matched', 'completed', 'cancelled') DEFAULT 'open',
    ai_detected_skill VARCHAR(100),           -- Skill extracted by Gemini AI
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- AI MATCHES TABLE
-- Stores AI matching results
-- ============================================
CREATE TABLE IF NOT EXISTS ai_matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    worker_id INT NOT NULL,
    match_score DECIMAL(5,2) DEFAULT 0.00,   -- AI confidence score (0-100)
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE
);

-- ============================================
-- RATINGS TABLE
-- Client ratings for workers
-- ============================================
CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    client_id INT NOT NULL,
    worker_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (worker_id) REFERENCES workers(id) ON DELETE CASCADE
);

-- ============================================
-- SEED DATA — Sample Workers for Testing
-- Password for ALL seed accounts: password123
-- Hash generated with Werkzeug generate_password_hash()
-- ============================================
INSERT INTO users (name, email, password, role, phone, city) VALUES
('Ramesh Kumar',      'ramesh@test.com', 'scrypt:32768:8:1$Naa7NbJrD3FSEDfw$4574f40c0b085914270d56205e63ddabf077445a6a4002f31d4b89d4f2233f3f6b35c9e3cf53586a56689e8c117561226a89030a15befd502711d49f263fa2e1', 'worker', '9876543210', 'Bhopal'),
('Suresh Yadav',      'suresh@test.com', 'scrypt:32768:8:1$Naa7NbJrD3FSEDfw$4574f40c0b085914270d56205e63ddabf077445a6a4002f31d4b89d4f2233f3f6b35c9e3cf53586a56689e8c117561226a89030a15befd502711d49f263fa2e1', 'worker', '9876543211', 'Bhopal'),
('Mohan Patel',       'mohan@test.com',  'scrypt:32768:8:1$Naa7NbJrD3FSEDfw$4574f40c0b085914270d56205e63ddabf077445a6a4002f31d4b89d4f2233f3f6b35c9e3cf53586a56689e8c117561226a89030a15befd502711d49f263fa2e1', 'worker', '9876543212', 'Bhopal'),
('Dinesh Vishwakarma','dinesh@test.com', 'scrypt:32768:8:1$Naa7NbJrD3FSEDfw$4574f40c0b085914270d56205e63ddabf077445a6a4002f31d4b89d4f2233f3f6b35c9e3cf53586a56689e8c117561226a89030a15befd502711d49f263fa2e1', 'worker', '9876543213', 'Bhopal'),
('Priya Sahu',        'priya@test.com',  'scrypt:32768:8:1$Naa7NbJrD3FSEDfw$4574f40c0b085914270d56205e63ddabf077445a6a4002f31d4b89d4f2233f3f6b35c9e3cf53586a56689e8c117561226a89030a15befd502711d49f263fa2e1', 'worker', '9876543214', 'Bhopal'),
('Ajay Malviya',      'ajay@test.com',   'scrypt:32768:8:1$Naa7NbJrD3FSEDfw$4574f40c0b085914270d56205e63ddabf077445a6a4002f31d4b89d4f2233f3f6b35c9e3cf53586a56689e8c117561226a89030a15befd502711d49f263fa2e1', 'worker', '9876543215', 'Bhopal');

INSERT INTO workers (user_id, skill_category, experience_years, address, description, availability, rating, total_jobs) VALUES
(1, 'Plumber',     8, 'Arera Colony, Bhopal',       'Expert in pipe fitting, leak repair, bathroom fittings.',     'available', 4.5, 120),
(2, 'Electrician', 5, 'MP Nagar, Bhopal',            'Wiring, MCB, inverter installation specialist.',              'available', 4.2,  95),
(3, 'Carpenter',   10,'Shahpura, Bhopal',             'Furniture making, door/window fitting, wood polish.',         'available', 4.8, 200),
(4, 'Painter',     6, 'Kolar Road, Bhopal',           'Interior/exterior painting, waterproofing, texture coating.', 'busy',      4.0,  78),
(5, 'Cleaner',     3, 'Hoshangabad Road, Bhopal',    'Deep house cleaning, sofa cleaning, pest control.',           'available', 4.3,  55),
(6, 'AC Mechanic', 7, 'Bhopal Junction Area, Bhopal','AC installation, gas refilling, servicing all brands.',       'available', 4.6, 145);
