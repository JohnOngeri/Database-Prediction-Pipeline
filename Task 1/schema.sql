-- Create Database
CREATE DATABASE IF NOT EXISTS student_performance;
USE student_performance;

-- Table: Students (contains all demographic data from CSV)
CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    gender ENUM('male', 'female') NOT NULL,
    race_ethnicity ENUM('group A', 'group B', 'group C', 'group D', 'group E') NOT NULL,
    parental_level_of_education ENUM(
        'some high school',
        'high school',
        'some college',
        'associate''s degree',
        'bachelor''s degree',
        'master''s degree'
    ) NOT NULL,
    lunch ENUM('standard', 'free/reduced') NOT NULL,
    test_preparation ENUM('completed', 'none') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Exams (contains all score data from CSV)
CREATE TABLE Exams (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    math_score INT CHECK (math_score BETWEEN 0 AND 100),
    reading_score INT CHECK (reading_score BETWEEN 0 AND 100),
    writing_score INT CHECK (writing_score BETWEEN 0 AND 100),
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

-- Table: ExamAuditLog (for tracking changes, not in original dataset)
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

-- Stored Procedure: Add complete student record from CSV data
DELIMITER //
CREATE PROCEDURE AddStudentRecord(
    IN p_gender VARCHAR(10),
    IN p_race VARCHAR(20),
    IN p_parent_edu VARCHAR(50),
    IN p_lunch VARCHAR(20),
    IN p_test_prep VARCHAR(20),
    IN p_math_score INT,
    IN p_reading_score INT,
    IN p_writing_score INT
)
BEGIN
    DECLARE v_student_id INT;
    
    -- Insert student (all demographic fields from CSV)
    INSERT INTO Students (gender, race_ethnicity, parental_level_of_education, lunch, test_preparation)
    VALUES (p_gender, p_race, p_parent_edu, p_lunch, p_test_prep);
    
    SET v_student_id = LAST_INSERT_ID();
    
    -- Insert exam scores (all score fields from CSV)
    INSERT INTO Exams (student_id, math_score, reading_score, writing_score)
    VALUES (v_student_id, p_math_score, p_reading_score, p_writing_score);
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

-- Sample Data from CSV (first 3 records)
CALL AddStudentRecord('female', 'group B', 'bachelor''s degree', 'standard', 'none', 72, 72, 74);
CALL AddStudentRecord('female', 'group C', 'some college', 'standard', 'completed', 69, 90, 88);
CALL AddStudentRecord('female', 'group B', 'master''s degree', 'standard', 'none', 90, 95, 93);