import random
from datetime import date, timedelta

from faker import Faker
from sqlalchemy.exc import IntegrityError

from database import get_session
from models import Group, Teacher, Student, Subject, Grade

fake = Faker("uk_UA")

GROUPS = ["КН-21", "КН-22", "КН-23"]
SUBJECTS = [
    "Математичний аналіз",
    "Лінійна алгебра",
    "Програмування на Python",
    "Бази даних",
    "Операційні системи",
    "Комп'ютерні мережі",
    "Алгоритми та структури даних",
]
NUM_TEACHERS = 4
NUM_STUDENTS = 40
MAX_GRADES_PER_STUDENT = 20


def seed():
    session = get_session()
    try:
        # 1. Create groups
        groups = []
        for name in GROUPS:
            g = Group(name=name)
            session.add(g)
            groups.append(g)
        session.flush()

        # 2. Create teachers
        teachers = []
        for _ in range(NUM_TEACHERS):
            t = Teacher(fullname=fake.name())
            session.add(t)
            teachers.append(t)
        session.flush()

        # 3. Create subjects (assign random teacher)
        subjects = []
        for name in SUBJECTS:
            s = Subject(name=name, teacher_id=random.choice(teachers).id)
            session.add(s)
            subjects.append(s)
        session.flush()

        # 4. Create students
        students = []
        for _ in range(NUM_STUDENTS):
            st = Student(
                fullname=fake.name(),
                group_id=random.choice(groups).id,
            )
            session.add(st)
            students.append(st)
        session.flush()

        # 5. Create grades (up to 20 per student across all subjects)
        start_date = date(2024, 9, 1)
        end_date = date(2025, 6, 30)

        for student in students:
            # Randomly pick subjects for this student (at least all of them)
            num_grades = random.randint(15, MAX_GRADES_PER_STUDENT)
            subject_pool = subjects * 3  # allow duplicates / multiple grades per subject
            chosen = random.sample(subject_pool, k=min(num_grades, len(subject_pool)))

            for subj in chosen:
                days_delta = (end_date - start_date).days
                rand_date = start_date + timedelta(days=random.randint(0, days_delta))
                gr = Grade(
                    grade=round(random.uniform(60, 100), 1),
                    date_of=rand_date,
                    student_id=student.id,
                    subject_id=subj.id,
                )
                session.add(gr)

        session.commit()
        print("Database seeded successfully!")
        print(f"  Groups: {len(groups)}")
        print(f"  Teachers: {len(teachers)}")
        print(f"  Subjects: {len(subjects)}")
        print(f"  Students: {len(students)}")

    except IntegrityError as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
