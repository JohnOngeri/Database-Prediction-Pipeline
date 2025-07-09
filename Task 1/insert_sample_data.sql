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
