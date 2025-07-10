-- Create Database
CREATE DATABASE IF NOT EXISTS student_performance;
USE student_performance;

-- Table: Students
CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    gender ENUM('male', 'female') NOT NULL,
    race_ethnicity ENUM('group A', 'group B', 'group C', 'group D', 'group E') NOT NULL,
    parental_level_of_education ENUM(
        'some high school',
        'high school',
        'some college',
        'associate\'s degree',
        'bachelor\'s degree',
        'master\'s degree'
    ) NOT NULL,
    lunch ENUM('standard', 'free/reduced') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Exams
CREATE TABLE Exams (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    math_score INT CHECK (math_score BETWEEN 0 AND 100),
    reading_score INT CHECK (reading_score BETWEEN 0 AND 100),
    writing_score INT CHECK (writing_score BETWEEN 0 AND 100),
    exam_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

-- Table: TestPreparation
CREATE TABLE TestPreparation (
    preparation_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completion_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

-- Table: ExamAuditLog
CREATE TABLE ExamAuditLog (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_id INT NOT NULL,
    action_type ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    old_math_score INT,
    new_math_score INT,
    old_reading_score INT,
    new_reading_score INT,
    old_writing_score INT,
    new_writing_score INT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(50) DEFAULT CURRENT_USER,
    FOREIGN KEY (exam_id) REFERENCES Exams(exam_id)
);

-- Stored Procedure: Add complete student record
DELIMITER //
CREATE PROCEDURE AddStudentWithScores(
    IN p_gender VARCHAR(10),
    IN p_race VARCHAR(20),
    IN p_parent_edu VARCHAR(50),
    IN p_lunch VARCHAR(20),
    IN p_test_prep BOOLEAN,
    IN p_math_score INT,
    IN p_reading_score INT,
    IN p_writing_score INT,
    IN p_exam_date DATE
)
BEGIN
    DECLARE v_student_id INT;
    
    -- Insert student
    INSERT INTO Students (gender, race_ethnicity, parental_level_of_education, lunch)
    VALUES (p_gender, p_race, p_parent_edu, p_lunch);
    
    SET v_student_id = LAST_INSERT_ID();
    
    -- Insert exam scores
    INSERT INTO Exams (student_id, math_score, reading_score, writing_score, exam_date)
    VALUES (v_student_id, p_math_score, p_reading_score, p_writing_score, p_exam_date);
    
    -- Insert test preparation
    INSERT INTO TestPreparation (student_id, course_completed)
    VALUES (v_student_id, p_test_prep);
END //
DELIMITER ;

-- Trigger: Log exam score changes
DELIMITER //
CREATE TRIGGER after_exam_update
AFTER UPDATE ON Exams
FOR EACH ROW
BEGIN
    IF OLD.math_score != NEW.math_score OR 
       OLD.reading_score != NEW.reading_score OR 
       OLD.writing_score != NEW.writing_score THEN
       
        INSERT INTO ExamAuditLog (
            exam_id,
            action_type,
            old_math_score,
            new_math_score,
            old_reading_score,
            new_reading_score,
            old_writing_score,
            new_writing_score
        ) VALUES (
            NEW.exam_id,
            'UPDATE',
            OLD.math_score,
            NEW.math_score,
            OLD.reading_score,
            NEW.reading_score,
            OLD.writing_score,
            NEW.writing_score
        );
    END IF;
END //
DELIMITER ;

-- Sample Data
CALL AddStudentWithScores('female', 'group D', 'bachelor''s degree', 'standard', TRUE, 72, 72, 74, '2023-01-15');
CALL AddStudentWithScores('male', 'group A', 'some college', 'free/reduced', FALSE, 69, 90, 88, '2023-01-15');
CALL AddStudentWithScores('female', 'group C', 'high school', 'standard', TRUE, 90, 95, 93, '2023-01-16');