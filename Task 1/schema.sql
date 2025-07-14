-- Create Database
CREATE DATABASE IF NOT EXISTS student_performance;
USE student_performance;

-- Table: Students (demographics, excluding test_preparation)
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: TestPreparation (now separate)
CREATE TABLE TestPreparation (
    prep_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    status ENUM('completed', 'none') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

-- Table: Exams
CREATE TABLE Exams (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    math_score INT CHECK (math_score BETWEEN 0 AND 100),
    reading_score INT CHECK (reading_score BETWEEN 0 AND 100),
    writing_score INT CHECK (writing_score BETWEEN 0 AND 100),
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

-- Table: ExamAuditLog (FIXED - Removed DEFAULT USER())
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
    changed_by VARCHAR(50),  -- Removed DEFAULT USER() as it's not allowed
    FOREIGN KEY (exam_id) REFERENCES Exams(exam_id)
);

-- Stored Procedure: Add Student with Test Prep and Exam Scores
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

    -- Insert student
    INSERT INTO Students (gender, race_ethnicity, parental_level_of_education, lunch)
    VALUES (p_gender, p_race, p_parent_edu, p_lunch);

    SET v_student_id = LAST_INSERT_ID();

    -- Insert test preparation status
    INSERT INTO TestPreparation (student_id, status)
    VALUES (v_student_id, p_test_prep);

    -- Insert exam scores
    INSERT INTO Exams (student_id, math_score, reading_score, writing_score)
    VALUES (v_student_id, p_math_score, p_reading_score, p_writing_score);
END //
DELIMITER ;

-- Trigger: Log exam score changes (Updated to handle changed_by)
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
            new_writing_score,
            changed_by,
            changed_at
        ) VALUES (
            NEW.exam_id,
            'UPDATE',
            OLD.math_score,
            NEW.math_score,
            OLD.reading_score,
            NEW.reading_score,
            OLD.writing_score,
            NEW.writing_score,
            CURRENT_USER,  -- Using CURRENT_USER here instead of DEFAULT
            CURRENT_TIMESTAMP
        );
    END IF;
END //
DELIMITER ;

-- Sample Data (3 Records)
CALL AddStudentRecord('female', 'group B', 'bachelor''s degree', 'standard', 'none', 72, 72, 74);
CALL AddStudentRecord('female', 'group C', 'some college', 'standard', 'completed', 69, 90, 88);
CALL AddStudentRecord('female', 'group B', 'master''s degree', 'standard', 'none', 90, 95, 93);