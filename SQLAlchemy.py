from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, and_
from sqlalchemy import desc

engine = create_engine("mysql+mysqlconnector://root:Maksim21z*@localhost/students", echo=True)
meta = MetaData(engine)

student = Table('student', meta, autoload=True)
teacher = Table('teacher', meta, autoload=True)
training_course = Table('training_course', meta, autoload=True)
exam = Table('exam', meta, autoload=True)
exam_result = Table('exam_result', meta, autoload=True)
student_result = Table('student_result', meta, autoload=True)
session = sessionmaker(bind=engine)
s = session()

class Student():
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


mapper(Student, student)


class Teacher():
    def __init__(self, id, first_name, last_name, result_exam):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.result_exam = result_exam


mapper(Teacher, teacher)


class Trainig_course():
    def __init__(self, id, name, teacher_id):
        self.id = id
        self.name = name
        self.teacher_id = teacher_id


mapper(Trainig_course, training_course)


class Exam():
    def __init__(self, id, date, teacher_id, training_course_id):
        self.id = id
        self.date = date
        self.teacher_id = teacher_id
        self.training_course_id = training_course_id


mapper(Exam, exam)


class Exam_result():
    def __init__(self, id, teacher_id, student_id, result, note, exam_id):
        self.id = id
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.result = result
        self.note = note
        self.exam_id = exam_id


mapper(Exam_result, exam_result)



# Выбрать имена и фамилии студентов, успешно сдавших экзамен, упорядоченных по результату экзамена (отличники первые в результате)
for row in s.query(Exam_result, Student).filter(Exam_result.student_id == Student.id).filter(
        Exam_result.result >= 4).order_by(Exam_result.result.desc()):
    print(row.Student.first_name, ' ', row.Student.last_name, ' ', row.Exam_result.result)

print('\n\n\n')
# Посчитать количество студентов, успешно сдавших экзамен больше 4
from sqlalchemy import func
print(s.query(func.count(Exam_result.id)).filter(Exam_result.result > 4).scalar())

#Посчитать количество студентов, сдавших экзамен “автоматом” (нет записи в таблице exam_result но есть положительный результат в таблице student_result)
print(s.query(func.count(Exam_result.id)).filter(Exam_result.note == '').scalar())

#Посчитать средний балл студентов по предмету с наименованием “Химия”
print(s.query(func.avg(Exam_result.result)).filter(Exam_result.exam_id == 5).all())

# Выбрать имена и фамилии студентов, не сдававших экхзамен по предмету “Теория графов” (2 вида запроса)

for row in s.query(Student, Exam_result).filter(Student.id == Exam_result.student_id).filter(Exam_result.result < 4):
    print(row.Student.first_name, ' ', row.Student.last_name)

#Выбрать идентификатор преподавателей, читающих лекции по больше чем по 2 предметам
for row in s.query(Trainig_course).filter(Trainig_course.id != Trainig_course.teacher_id):
    print(row.teacher_id)

#Выбрать идентификатор и фамилии студентов, пересдававших хотя бы 1 предмет(балл < 4 == пересдача)

for row in s.query(Exam_result, Student).filter(Exam_result.student_id == Student.id).filter(Exam_result.result < 4):
    print(row.Exam_result.student_id, ' ', row.Student.last_name)

#Вывести имена , фамилии, оценки 5 студентов с максимальными оценками
for row in s.query(Exam_result, Student).filter(Exam_result.student_id == Student.id).order_by(Exam_result.result.desc()).limit(5).all():
    print(row.Student.first_name,' ', row.Student.last_name,' ', row.Exam_result.result)


#Вывести фамилию преподавателя, у которого наилучшие результаты по его предметам


for row in s.query(Teacher).order_by(Teacher.result_exam.desc()).limit(1).all():
    print(row.last_name, ' ', row.result_exam)