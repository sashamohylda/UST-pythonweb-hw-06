"""
my_select.py — 10 SQL queries via SQLAlchemy ORM session.
"""

from sqlalchemy import func, desc, cast, Numeric

from database import get_session
from models import Student, Grade, Subject, Teacher, Group


def avg_round(column):
    """Helper: avg with round, compatible with PostgreSQL."""
    return func.round(cast(func.avg(column), Numeric(10, 2)), 2)


def select_1():
    """Find top 5 students with the highest average grade across all subjects."""
    session = get_session()
    try:
        result = (
            session.query(
                Student.fullname,
                avg_round(Grade.grade).label("avg_grade"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .group_by(Student.id, Student.fullname)
            .order_by(desc("avg_grade"))
            .limit(5)
            .all()
        )
        return result
    finally:
        session.close()


def select_2(subject_id: int):
    """Find the student with the highest average grade for a specific subject."""
    session = get_session()
    try:
        result = (
            session.query(
                Student.fullname,
                Subject.name.label("subject"),
                avg_round(Grade.grade).label("avg_grade"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.id == subject_id)
            .group_by(Student.id, Student.fullname, Subject.name)
            .order_by(desc("avg_grade"))
            .limit(1)
            .first()
        )
        return result
    finally:
        session.close()


def select_3(subject_id: int):
    """Find the average grade in each group for a specific subject."""
    session = get_session()
    try:
        result = (
            session.query(
                Group.name.label("group"),
                Subject.name.label("subject"),
                avg_round(Grade.grade).label("avg_grade"),
            )
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.id == subject_id)
            .group_by(Group.id, Group.name, Subject.name)
            .order_by(desc("avg_grade"))
            .all()
        )
        return result
    finally:
        session.close()


def select_4():
    """Find the overall average grade across all grades."""
    session = get_session()
    try:
        result = (
            session.query(
                avg_round(Grade.grade).label("avg_grade")
            )
            .scalar()
        )
        return result
    finally:
        session.close()


def select_5(teacher_id: int):
    """Find all courses (subjects) taught by a specific teacher."""
    session = get_session()
    try:
        result = (
            session.query(Subject.name, Teacher.fullname)
            .join(Teacher, Teacher.id == Subject.teacher_id)
            .filter(Teacher.id == teacher_id)
            .all()
        )
        return result
    finally:
        session.close()


def select_6(group_id: int):
    """Find the list of students in a specific group."""
    session = get_session()
    try:
        result = (
            session.query(Student.fullname, Group.name)
            .join(Group, Group.id == Student.group_id)
            .filter(Group.id == group_id)
            .order_by(Student.fullname)
            .all()
        )
        return result
    finally:
        session.close()


def select_7(group_id: int, subject_id: int):
    """Find grades of students in a specific group for a specific subject."""
    session = get_session()
    try:
        result = (
            session.query(
                Student.fullname,
                Subject.name.label("subject"),
                Grade.grade,
                Grade.date_of,
            )
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .join(Group, Group.id == Student.group_id)
            .filter(Group.id == group_id, Subject.id == subject_id)
            .order_by(Student.fullname, Grade.date_of)
            .all()
        )
        return result
    finally:
        session.close()


def select_8(teacher_id: int):
    """Find the average grade given by a specific teacher across their subjects."""
    session = get_session()
    try:
        result = (
            session.query(
                Teacher.fullname,
                avg_round(Grade.grade).label("avg_grade"),
            )
            .join(Subject, Subject.teacher_id == Teacher.id)
            .join(Grade, Grade.subject_id == Subject.id)
            .filter(Teacher.id == teacher_id)
            .group_by(Teacher.id, Teacher.fullname)
            .first()
        )
        return result
    finally:
        session.close()


def select_9(student_id: int):
    """Find all courses (subjects) attended by a specific student."""
    session = get_session()
    try:
        result = (
            session.query(Subject.name, Student.fullname)
            .join(Grade, Grade.subject_id == Subject.id)
            .join(Student, Student.id == Grade.student_id)
            .filter(Student.id == student_id)
            .distinct()
            .all()
        )
        return result
    finally:
        session.close()


def select_10(student_id: int, teacher_id: int):
    """Find courses taught by a specific teacher that a specific student attends."""
    session = get_session()
    try:
        result = (
            session.query(Subject.name, Student.fullname, Teacher.fullname.label("teacher"))
            .join(Grade, Grade.subject_id == Subject.id)
            .join(Student, Student.id == Grade.student_id)
            .join(Teacher, Teacher.id == Subject.teacher_id)
            .filter(Student.id == student_id, Teacher.id == teacher_id)
            .distinct()
            .all()
        )
        return result
    finally:
        session.close()


def select_11(teacher_id: int, student_id: int):
    """BONUS: Average grade that a specific teacher gives to a specific student."""
    session = get_session()
    try:
        result = (
            session.query(
                Teacher.fullname.label("teacher"),
                Student.fullname.label("student"),
                avg_round(Grade.grade).label("avg_grade"),
            )
            .join(Subject, Subject.teacher_id == Teacher.id)
            .join(Grade, Grade.subject_id == Subject.id)
            .join(Student, Student.id == Grade.student_id)
            .filter(Teacher.id == teacher_id, Student.id == student_id)
            .group_by(Teacher.fullname, Student.fullname)
            .first()
        )
        return result
    finally:
        session.close()


def select_12(group_id: int, subject_id: int):
    """BONUS: Grades of students in a group for a subject at the last class."""
    session = get_session()
    try:
        subq = (
            session.query(func.max(Grade.date_of))
            .join(Student, Student.id == Grade.student_id)
            .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
            .scalar_subquery()
        )
        result = (
            session.query(
                Student.fullname,
                Subject.name.label("subject"),
                Grade.grade,
                Grade.date_of,
            )
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(
                Student.group_id == group_id,
                Grade.subject_id == subject_id,
                Grade.date_of == subq,
            )
            .all()
        )
        return result
    finally:
        session.close()


if __name__ == "__main__":
    print("=== select_1: Top 5 students by average grade ===")
    for row in select_1():
        print(row)

    print("\n=== select_2: Best student for subject_id=1 ===")
    print(select_2(1))

    print("\n=== select_3: Avg grade by group for subject_id=1 ===")
    for row in select_3(1):
        print(row)

    print("\n=== select_4: Overall average grade ===")
    print(select_4())

    print("\n=== select_5: Subjects by teacher_id=1 ===")
    for row in select_5(2):
        print(row)

    print("\n=== select_6: Students in group_id=1 ===")
    for row in select_6(1):
        print(row)

    print("\n=== select_7: Grades in group_id=1 for subject_id=1 ===")
    for row in select_7(1, 1):
            print(row)

    print("\n=== select_8: Avg grade given by teacher_id=1 ===")
    print(select_8(2))

    print("\n=== select_9: Subjects attended by student_id=1 ===")
    for row in select_9(1):
        print(row)

    print("\n=== select_10: Subjects for student_id=1 taught by teacher_id=1 ===")
    for row in select_10(1, 2):
        print(row)
