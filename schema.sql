-- Create the database and use it
CREATE DATABASE IF NOT EXISTS student_performance;
USE student_performance;

-- Table 1: students
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(10),
    race_ethnicity VARCHAR(20),
    parental_education VARCHAR(50),
    lunch VARCHAR(30),
    test_preparation_course VARCHAR(30)
);

-- Table 2: scores
CREATE TABLE scores (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    math_score INT,
    reading_score INT,
    writing_score INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Table 3: performance
CREATE TABLE performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    performance_level VARCHAR(20),
    predicted_pass BOOLEAN,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Sample test data
INSERT INTO students (gender, race_ethnicity, parental_education, lunch, test_preparation_course)
VALUES
('female', 'group B', 'bachelor\'s degree', 'standard', 'none'),
('male', 'group C', 'some college', 'free/reduced', 'completed');

INSERT INTO scores (student_id, math_score, reading_score, writing_score)
VALUES
(1, 72, 72, 74),
(2, 69, 90, 88);

INSERT INTO performance (student_id, performance_level, predicted_pass)
VALUES
(1, 'Good', TRUE),
(2, 'Average', TRUE);
