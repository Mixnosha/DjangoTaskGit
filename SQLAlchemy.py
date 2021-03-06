from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, and_
from sqlalchemy import desc
import time

engine = create_engine("mysql+mysqlconnector://root:password@localhost/students", echo=True)
meta = MetaData(engine)

student = Table('student', meta, autoload=True)
teacher = Table('teacher', meta, autoload=True)
training_course = Table('training_course', meta, autoload=True)
exam = Table('exam', meta, autoload=True)
exam_result = Table('exam_result', meta, autoload=True)
student_result = Table('student_result', meta, autoload=True)
session = sessionmaker(bind=engine)
s = session()


# Декоратор для подсчета времени выполнения запроса
def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print ("Время выполнения функции: %f" % (time.time()-t))
        return res

    return tmp


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

#Select the first and last names of the students who successfully passed the exam, sorted by the exam result (the first honors in the result)
@timer
def inquiry():
    list = []
    for row in s.query(Exam_result, Student).filter(Exam_result.student_id == Student.id).filter(
            Exam_result.result >= 4).order_by(Exam_result.result.desc()):
        list.append([row.Student.first_name, row.Student.last_name, row.Exam_result.result])
    return list


'''
Время выполнения функции: 0.018776
[['Александр', 'Бородич', 9],
['Александр', 'Беляев', 9],
['Александр', 'Беляев', 8],
['Богдан', 'Галаховский', 8], 
['Павел', 'Басенков', 8],
['Даниил', 'Адамович', 8],
['Даниил', 'Адамович', 8],
['Александр', 'Бородич', 8],
['Александр', 'Беляев', 8],
['Даниил', 'Адамович', 8],
['Александр', 'Бородич', 7],
['Александр', 'Беляев', 7],
['Павел', 'Басенков', 7],
['Александр', 'Бородич', 7],
['Даниил', 'Адамович', 6],
['Даниил', 'Адамович', 6],
['Алексей', 'Варкович', 6],
['Богдан', 'Галаховский', 6],
['Богдан', 'Галаховский', 6],
['Павел', 'Басенков', 6],
['Павел', 'Басенков', 6],
['Павел', 'Басенков', 5],
['Александр', 'Беляев', 5],
['Александр', 'Беляев', 4], 
['Александр', 'Бородич', 4], 
['Алексей', 'Варкович', 4], 
['Александр', 'Бородич', 4],
['Даниил', 'Адамович', 4]]
'''
#Count the number of students who successfully passed the exam above 4
from sqlalchemy import func
@timer
def inquiry2():
    return [s.query(func.count(Exam_result.id)).filter(Exam_result.result > 4).scalar()]

'''
Время выполнения функции: 0.024079
[23]
'''
#Count the number of students who passed the exam automatically (there is no entry in the exam_result table)
@timer
def inquiry3():
    return [s.query(func.count(Exam_result.id)).filter(Exam_result.note == '').scalar()]

'''
Время выполнения функции: 0.010621
[3]
'''
#Calculate the average score of students in the subject with the name "chemistry"
@timer
def inquiry4():
    return s.query(func.avg(Exam_result.result)).filter(Exam_result.exam_id == 5).all()[0][0]
'''
Время выполнения функции: 0.011171
4.0000
'''

#Select the first and last names of students who did not pass the exam (2 types of request)
@timer
def inquiry5():
    list = []
    for row in s.query(Student, Exam_result).filter(Student.id == Exam_result.student_id).filter(Exam_result.result < 4):
        list.append([row.Student.first_name, row.Student.last_name])
    return list

'''
Время выполнения функции: 0.024847
[['Павел', 'Басенков'],
['Алексей', 'Варкович'],
['Алексей', 'Варкович'],
['Алексей', 'Варкович'],
['Богдан', 'Галаховский'],
['Богдан', 'Галаховский'],
['Алексей', 'Варкович'],
['Богдан', 'Галаховский']]
'''
@timer
def inquiry5_2():
    list = []
    for row in s.query(Student, Exam_result).filter(Student.id == Exam_result.student_id).filter(
            Exam_result.note == 'не сдал'):
        list.append([row.Student.first_name, row.Student.last_name])
    return list

'''Время выполнения функции: 0.013200
[['Павел', 'Басенков'],
['Алексей', 'Варкович'],
['Алексей', 'Варкович'],
['Алексей', 'Варкович'],
['Богдан', 'Галаховский'],
['Богдан', 'Галаховский'],
['Алексей', 'Варкович'],
['Богдан', 'Галаховский']]
'''



#Select the identifier of teachers lecturing in more than 2 subjects
@timer
def inquiry6():
    list = []
    for row in s.query(Trainig_course).filter(Trainig_course.id != Trainig_course.teacher_id):
        list.append([row.teacher_id])
    return list

'''
Время выполнения функции: 0.046913
[]
'''
#Select the identifier and surnames of students who retried at least 1 subject
@timer
def inquiry7():
    list = []
    for row in s.query(Exam_result, Student).filter(Exam_result.student_id == Student.id).filter(Exam_result.result < 4):
        list.append([row.Exam_result.student_id, row.Student.last_name])
    return list

'''Время выполнения функции: 0.016161
[[2, 'Басенков'],
[5, 'Варкович'],
[5, 'Варкович'],
[5, 'Варкович'],
[6, 'Галаховский'],
[6, 'Галаховский'],
[5, 'Варкович'], 
[6, 'Галаховский']]

'''

#Display the first and last names of the 5 students with the highest grades
@timer
def inquiry8():
    list = []
    for row in s.query(Exam_result, Student).filter(Exam_result.student_id == Student.id).order_by(Exam_result.result.desc()).limit(5).all():
        list.append([row.Student.first_name, row.Student.last_name, row.Exam_result.result])
    return list


'''
Время выполнения функции: 0.012730
[['Александр', 'Бородич', 9],
['Александр', 'Беляев', 9],
['Даниил', 'Адамович', 8],
['Богдан', 'Галаховский', 8], 
['Павел', 'Басенков', 8]]

'''

#Display the name of the teacher who has the best results in his subjects
@timer
def inquiry10():
    return s.query(Teacher.last_name, func.avg(Exam_result.result)).filter(Exam_result.teacher_id == Teacher.id).\
        group_by(Exam_result.exam_id).order_by(func.avg(Exam_result.result).desc()).limit(1).all()
'''Время выполнения функции: 0.015626
[('Шепетюк', Decimal('7.3333'))]'''




