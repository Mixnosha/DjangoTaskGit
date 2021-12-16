
CREATE DATABASE students
    CHARACTER SET 'utf8'
    COLLATE 'utf8_general_ci';

USE students;
CREATE TABLE student (
  id int(11) unsigned NOT NULL,
  first_name varchar(20) NOT NULL,
  last_name varchar(20) NOT NULL,
  -- birth_date date NOT NULL,
  -- sex bit(1) NOT NULL,
  -- hostel_live bit(1) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Предмет
CREATE TABLE training_course (
  id INTEGER(11) UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
  name VARCHAR(50) NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB;

-- Преподаватель
CREATE TABLE teacher (
  id INTEGER(11) UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

-- Исправляем ошибки в таблице student
ALTER TABLE students.student CHANGE COLUMN id id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT ;
ALTER TABLE students.training_course ADD COLUMN teacher_id INT(11) UNSIGNED NOT NULL  AFTER name ,
  ADD CONSTRAINT teacher_fk
  FOREIGN KEY (teacher_id )
  REFERENCES students.teacher (id )
  ON DELETE CASCADE
  ON UPDATE RESTRICT
, ADD INDEX teacher_fk_idx (teacher_id ASC) ;
CREATE  TABLE students.exam (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  date TIMESTAMP NOT NULL ,
  PRIMARY KEY (id) ,
  UNIQUE INDEX id_UNIQUE (id ASC) );

ALTER TABLE students.exam ADD COLUMN teacher_id INT(11) UNSIGNED NOT NULL,
  ADD CONSTRAINT exam_teacher_fk
  FOREIGN KEY (teacher_id )
  REFERENCES students.teacher (id )
  ON DELETE RESTRICT
  ON UPDATE RESTRICT
, ADD INDEX exam_teacher_fk_idx (teacher_id ASC) ;

ALTER TABLE students.exam ADD COLUMN training_course_id INT(11) UNSIGNED NOT NULL,
  ADD CONSTRAINT exam_training_course_fk
  FOREIGN KEY (training_course_id )
  REFERENCES students.training_course (id )
  ON DELETE RESTRICT
  ON UPDATE RESTRICT
, ADD INDEX exam_training_course_fk_idx (training_course_id ASC) ;

CREATE  TABLE students.exam_result (
  id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT ,
  teacher_id INT(11) UNSIGNED NOT NULL ,
  student_id INT(11) UNSIGNED NOT NULL ,
  result TINYINT NOT NULL ,
  note VARCHAR(50) NULL ,
  PRIMARY KEY (id) ,
  INDEX exam_result_teacher_fk_idx (teacher_id ASC) ,
  INDEX exam_result_student_fk_idx (student_id ASC) ,
  CONSTRAINT exam_result_teacher_fk
    FOREIGN KEY (teacher_id )
    REFERENCES students.teacher (id )
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT exam_result_student_fk
    FOREIGN KEY (student_id )
    REFERENCES students.student (id )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE  TABLE students.student_result (
  student_id INT(11) UNSIGNED NOT NULL ,
  training_course_id INT(11) UNSIGNED NOT NULL ,
  exam_id INT(11) UNSIGNED,
  result TINYINT NOT NULL ,
  note VARCHAR(50) NULL ,
  INDEX student_result__idx (training_course_id ASC) ,
  INDEX student_result_student_id_idx (student_id ASC) ,
  CONSTRAINT student_result_training_course
    FOREIGN KEY (training_course_id )
    REFERENCES students.training_course (id )
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT student_result_student_id
    FOREIGN KEY (student_id )
    REFERENCES students.student (id )
    ON DELETE RESTRICT
    ON UPDATE RESTRICT);

ALTER TABLE students.exam_result ADD COLUMN exam_id INT(11) UNSIGNED NOT NULL  AFTER note ,
  ADD CONSTRAINT exam_result_exam_fk
  FOREIGN KEY (exam_id )
  REFERENCES students.exam (id )
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
  ADD INDEX exam_result_exam_fk_idx (exam_id ASC) ;

ALTER TABLE students.student_result
  ADD CONSTRAINT student_result_exam_fk
  FOREIGN KEY (exam_id )
  REFERENCES students.exam (id )
, ADD INDEX student_result_exam_fk_idx (exam_id ASC) ;




INSERT INTO student (first_name , last_name )
    VALUES ('Даниил' , 'Адамович' ),
           ('Павел' , 'Басенков'),
           ('Александр' , 'Беляев'),
           ('Александр' , 'Бородич'),
           ('Алексей' , 'Варкович'),
           ('Богдан' , 'Галаховский');


INSERT INTO teacher (first_name , last_name )
    VALUES ('Николай' , 'Рачковский' ),
           ('Наталья' , 'Рожнова'),
           ('Виталий' , 'Шепетюк'),
           ('Вячеслав' , 'Шестакович'),
           ('Инга' , 'Бычек'),
           ('Владимир' , 'Столер');

INSERT INTO training_course (name ,training_course.teacher_id )
    VALUES ('ЛаиАг' , 1  ),
           ('ППВГ' ,  2),
           ('Философия' ,3 ),
           ('ОАиП' , 4),
           ('Химия' , 5),
           ('Икг' ,6 );




INSERT INTO exam ( date , students.exam.teacher_id , students.exam.training_course_id)
    VALUES ('2022-01-06 9:00' , 1 ,1),
           ('2022-01-25 9:00' ,2 ,2),
           ('2022-01-21 9:00' ,3 ,3),
           ('2022-01-12 9:00' ,4 ,4),
           ('2022-01-17 9:00' ,5 ,5),
           ('2022-01-30 9:00' ,6 ,6);



INSERT INTO exam_result (exam_result.teacher_id , exam_result.student_id ,

                           exam_result.result, exam_result.note,
                           exam_result.exam_id)
    VALUES (1, 1 , 6, 'сдал', 1),
           (1, 2 , 3, 'не сдал', 1),
           (1, 3 , 8, 'сдал', 1),
           (1, 4 , 7, 'сдал', 1),
           (1, 5 , 1, 'не сдал', 1),
           (1, 6 , 6, 'сдал', 1);


INSERT INTO student_result(student_id , training_course_id , exam_id , result , note)
    VALUES (1 , 1 , 1 , 4 , 'сдал'),
           (2 , 1 , 1 , 6 , 'сдал'),
           (3 , 1 , 1 , 7 , 'сдал'),
           (4 , 1 , 1 , 1 , 'не сдал'),
           (5 , 1 , 1 , 2 , 'не сдал'),
           (6 , 1 , 1 , 6 , 'сдал');



INSERT INTO exam_result (exam_result.teacher_id , exam_result.student_id ,

                           exam_result.result, exam_result.note,
                           exam_result.exam_id)
    VALUES (6, 1 , 8, 'сдал', 6),
           (6, 2 , 6, 'сдал', 6),
           (6, 3 , 8, '', 6),
           (6, 4 , 4, 'сдал', 6),
           (6, 5 , 3, 'не сдал', 6),
           (6, 6 , 6, 'сдал', 6);


INSERT INTO student_result(student_id , training_course_id , exam_id , result , note)
    VALUES (1 , 6 , 6 , 7 , 'сдал'),
           (2 , 6 , 6 , 6 , 'сдал'),
           (3 , 6 , 6 , 8 , 'сдал'),
           (4 , 6 , 6 , 5, 'сдал'),
           (5 , 6 , 6 , 4 , 'сдал'),
           (6 , 6 , 6 , 5, 'сдал');

#Собственно запросы
#Выбрать имена и фамилии студентов, успешно сдавших экзамен, упорядоченных по результату экзамена (отличники первые в результате)
SELECT student.first_name, student.last_name, exam_result.result
    FROM exam_result  INNER JOIN student
    ON student.id = exam_result.student_id
    WHERE exam_result.result >= 4 ORDER BY exam_result.result DESC;

#Посчитать количество студентов, успешно сдавших экзамен выше 5
SELECT COUNT(result) AS 'Кол-во студентов' FROM exam_result WHERE result >= 6

#Посчитать количество студентов, сдвших экзамен “автоматом” (нет записи в таблице exam_result.note)
SELECT COUNT(note) AS 'Кол-во студентов' FROM exam_result WHERE note = '';

#Посчитать средний балл студентов по предмету с наименованием “Химия”
SELECT AVG(result) AS 'средний балл Химия' FROM exam_result WHERE exam_id = 5;

#Выбрать имена и фамилии студентов, не сдававших экхзамен по предмету “Икг” (2 вида запроса)
#1
SELECT student.first_name, student.last_name, exam_result.result , exam_result.exam_id
    FROM exam_result  INNER JOIN student
    ON student.id = exam_result.student_id
    WHERE exam_result.result < 4 AND exam_result.exam_id = 6 ORDER BY exam_result.result DESC;
#2
SELECT student.first_name, student.last_name, exam_result.result , exam_result.exam_id
    FROM exam_result  INNER JOIN student
    ON student.id = exam_result.student_id
    WHERE exam_result.note = 'не сдал' AND exam_result.exam_id = 6 ORDER BY exam_result.result DESC;

#Выбрать идентификатор преподавателей, читающих лекции по больше чем по 1 предметам
SELECT teacher.last_name , training_course.teacher_id  AS 'ID Учителя'
    FROM training_course INNER JOIN teacher
    ON teacher.id = training_course.teacher_id
    WHERE training_course.id <> training_course.teacher_id ORDER BY training_course.teacher_id ;

# Выбрать идентификатор и фамилии студентов, пересдававших хотя бы 1 предмет (оценка меньше 4 == пересдача)
SELECT  exam_result.student_id , student.last_name, exam_result.result
    FROM exam_result INNER JOIN student
    ON exam_result.student_id = student.id
    WHERE exam_result.result < 4 ORDER BY exam_result.student_id

#Вывести имена и фамилии 5 студентов с максимальными оценками
SELECT  student.first_name , student.last_name , exam_result.result
    FROM exam_result INNER JOIN student
    ON exam_result.student_id = student.id
    ORDER BY exam_result.result DESC LIMIT 5;

#Вывести фамилию преподавателя, у которого наилучшие результаты по его предметам

ALTER TABLE students.teacher ADD COLUMN result_exam FLOAT  AFTER last_name

SELECT AVG(result) FROM exam_result WHERE exam_id = 1; #5.16
SELECT AVG(result) FROM exam_result WHERE exam_id = 2; #6.16
SELECT AVG(result) FROM exam_result WHERE exam_id = 3; #7.33
SELECT AVG(result) FROM exam_result WHERE exam_id = 4; #5.16
SELECT AVG(result) FROM exam_result WHERE exam_id = 5; #3.5
SELECT AVG(result) FROM exam_result WHERE exam_id = 6; #5.83

UPDATE  teacher SET result_exam = 5.16 WHERE id = 1;
UPDATE  teacher SET result_exam = 6.16 WHERE id = 2;
UPDATE  teacher SET result_exam = 7.33 WHERE id = 3;
UPDATE  teacher SET result_exam = 5.16 WHERE id = 4;
UPDATE  teacher SET result_exam = 3.5 WHERE id = 5;
UPDATE  teacher SET result_exam = 5.83 WHERE id = 6;

SELECT last_name , result_exam FROM teacher ORDER BY result_exam DESC LIMIT 1;
