-- Create Database
CREATE DATABASE IF NOT EXISTS student_performance;
USE student_performance;

-- Table: Students
CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(10),
    parental_level_of_education VARCHAR(100)
);

-- Table: Exams
CREATE TABLE Exams (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    math_score INT,
    reading_score INT,
    writing_score INT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Table: TestPreparationCourses
CREATE TABLE TestPreparationCourses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    test_preparation_course VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Sample Data
INSERT INTO Students (gender, parental_level_of_education)
VALUES
('female', 'bachelor’s degree'),
('male', 'some college'),
('female', 'high school');

INSERT INTO Exams (student_id, math_score, reading_score, writing_score)
VALUES
(1, 72, 72, 74),
(2, 69, 90, 88),
(3, 90, 95, 93);

INSERT INTO TestPreparationCourses (student_id, test_preparation_course)
VALUES
(1, 'none'),
(2, 'completed'),
(3, 'completed');

-- Stored Procedure: Add a new exam score
DELIMITER //
CREATE PROCEDURE AddExamScore(
    IN sid INT, IN math INT, IN reading INT, IN writing INT
)
BEGIN
    INSERT INTO Exams (student_id, math_score, reading_score, writing_score)
    VALUES (sid, math, reading, writing);
END;
//
DELIMITER ;

-- Trigger: Log when a new exam is inserted
CREATE TABLE ExamLog (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_exam_insert
AFTER INSERT ON Exams
FOR EACH ROW
BEGIN
    INSERT INTO ExamLog (exam_id) VALUES (NEW.exam_id);
END;
//
DELIMITER ;
