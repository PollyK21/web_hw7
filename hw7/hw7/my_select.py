from sqlalchemy import func
from sqlalchemy import create_engine, distinct
from sqlalchemy.orm import sessionmaker
from models import Groups, Students, Teachers, Subjects, Marks

engine = create_engine('postgresql://postgres:polly@localhost:5432/postgres')
DBSession = sessionmaker(bind=engine)
session = DBSession()


def select_1():
    subquery = session.query(Marks.student_id, func.avg(Marks.grade).label('average_grade')
    ).group_by(Marks.student_id).order_by(func.avg(Marks.grade).desc()).limit(5).subquery()

    query = session.query(Students.name, subquery.c.average_grade
    ).join(subquery, Students.id == subquery.c.student_id)
    results = query.all()

    for name, average_grade in results:
        print(f"Student: {name}, Average Grade: {average_grade}")


def select_2():
    subquery = session.query(
        Marks.student_id,
        Marks.subject_id,
        func.avg(Marks.grade).label('avg_grade')
    ).group_by(
        Marks.student_id, Marks.subject_id
    ).subquery()

    max_subquery = session.query(
        subquery.c.subject_id,
        func.max(subquery.c.avg_grade).label('max_avg_grade')
    ).group_by(
        subquery.c.subject_id
    ).subquery()

    query = session.query(
        Students.name.label('student_name'),
        Subjects.name.label('subject_name'),
        subquery.c.avg_grade.label('average_grade')
    ).join(
        subquery, Students.id == subquery.c.student_id
    ).join(
        max_subquery, (subquery.c.subject_id == max_subquery.c.subject_id) & (subquery.c.avg_grade == max_subquery.c.max_avg_grade)
    ).join(
        Subjects, Subjects.id == max_subquery.c.subject_id
    ).order_by(
        Subjects.name
    )

    results = query.all()
    for result in results:
        print(f"Subject: {result.subject_name}, Student: {result.student_name}, Average Grade: {result.average_grade}")


def select_3():
    query = session.query(
        Students.group_id.label('group_id'),
        Subjects.name.label('subject_name'),
        func.avg(Marks.grade).label('average_grade')).join(
            Marks, Marks.student_id == Students.id 
        ).join(Subjects, Subjects.id == Marks.subject_id
        ).group_by(Students.group_id,Subjects.name).order_by(Students.group_id, Subjects.name)
    results = query.all()
    for result in results:
        print(f"Group: {result.group_id}, Subject: {result.subject_name}, Average Grade: {result.average_grade}")


def select_4():
    query = session.query(func.avg(Marks.grade).label('average_grade'))
    results = query.all()
    for result in results:
        print(f"Average Grade: {result.average_grade}")


def select_5():
    subquery = session.query(Subjects.teacher_id, func.string_agg(Subjects.name, ",").label('course_names')
    ).filter(Teachers.id == Subjects.teacher_id
    ).group_by(Subjects.teacher_id).subquery()

    query = session.query(Teachers.name, subquery.c.course_names).join(
        subquery, Teachers.id == subquery.c.teacher_id
    )
    results = query.all()
    for result in results:
        print(f"Teacher: {result.name}, Courses: {result.course_names}")


def select_6():
    query = session.query(Students.name.label("Student"), Groups.group_code.label('Group'), Groups.id
    ).join(Groups, Groups.id == Students.group_id
    ).group_by(Students.name,Groups.group_code,Groups.id
    ).order_by(Groups.id)
    results = query.all()
    for result in results:
        print(f"Student: {result.Student}, Group: {result.Group}")             


def select_7():
    query = session.query(Groups.group_code.label("group_code"), Subjects.name.label("Subject"), Students.name.label("Student"), Marks.grade.label("Grade")
    ).join(Groups, Groups.id == Students.group_id
    ).join(Marks, Students.id == Marks.student_id
    ).join(Subjects, Marks.subject_id == Subjects.id
    ).group_by(Groups.group_code,Subjects.name,Students.name,Marks.grade,Groups.id
    ).order_by(Groups.id, Subjects.name
    )
    results = query.all()
    for result in results:
        print(f"Group: {result.group_code}, Subject: {result.Subject}, Student: {result.Student}, Grade: {result.Grade}") 


def select_8():
    query = session.query(Teachers.name, func.avg(Marks.grade)
    ).join(Subjects, Subjects.teacher_id == Teachers.id
    ).join(Marks, Marks.subject_id==Subjects.id
    ).group_by(Teachers.name)
    results = query.all()
    print(results)
    for result in results:
        print(f"Teacher: {result[0]}, average_grade: {result[1]}")


def select_9():
    query = session.query(
        Students.name,
        func.string_agg(distinct(Subjects.name), '; ').label('course_names')
        ).join(Marks, Marks.subject_id == Subjects.id
        ).group_by(
        Students.name)

    results = query.all()
    for result in results:
        print(f"Student: {result.name}, Course Names: {result.course_names}")


def select_10():
    query = session.query(
        Students.name.label('student_name'),
        Teachers.name.label('teacher_name'),
        func.string_agg(distinct(Subjects.name), '; ').label('course_names')
    ).join(
        Marks, Students.id == Marks.student_id
    ).join(
        Subjects, Marks.subject_id == Subjects.id
    ).join(
        Teachers, Subjects.teacher_id == Teachers.id
    ).group_by(
        Students.name, Teachers.name
    )

    # Получаем результаты запроса
    results = query.all()

    # Выводим результаты
    for res in results:
        print(f"Student:{res.student_name}, teacher: {res.teacher_name}, courses: {res.course_names}")

if __name__ == '__main__':
    print('------------ Select 1 ------------')
    select_1()

    print('------------ Select 2 ------------')
    select_2()

    print('------------ Select 3 ------------')
    select_3()

    print('------------ Select 4 ------------')
    select_4()

    print('------------ Select 5 ------------')
    select_5()

    print('------------ Select 6 ------------')
    select_6()

    print('------------ Select 7 ------------')
    select_7()

    print('------------ Select 8 ------------')
    select_8()

    print('------------ Select 9 ------------')
    select_9()

    print('------------ Select 10 ------------')
    select_10()
