import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Student
from database import SessionLocal, engine

# Функция для форматирования списка студентов
def format_students(students):
    """Функция для форматирования списка студентов."""
    return [
        f"Student(name='{student.name}', faculty='{student.faculty}', course='{student.course}', grade={student.grade})"
        for student in students
    ]

# Инициализация базы данных
def init_db():
    print("Инициализация базы данных...")
    from models import Base
    Base.metadata.create_all(bind=engine)

# Заполнение базы данных данными из CSV
def populate_db_from_csv(file_path: str):
    print("Заполнение базы данных из CSV...")
    df = pd.read_csv(file_path)
    print("Заголовки CSV:", df.columns)  # Вывод заголовков для проверки
    db = SessionLocal()
    for _, row in df.iterrows():
        student = Student(
            name=f"{row['Фамилия']} {row['Имя']}",  # Объединяем Фамилию и Имя
            faculty=row['Факультет'],
            course=row['Курс'],
            grade=row['Оценка']
        )
        db.add(student)
    db.commit()
    db.close()

# Получение списка студентов по названию факультета
def get_students_by_faculty(faculty: str):
    db = SessionLocal()
    students = db.query(Student).filter(Student.faculty == faculty).all()
    db.close()
    return students

# Получение списка уникальных курсов
def get_unique_courses():
    db = SessionLocal()
    courses = db.query(Student.course).distinct().all()
    db.close()
    return [course[0] for course in courses]

# Получение среднего балла по факультету
def get_average_grade_by_faculty(faculty: str):
    db = SessionLocal()
    avg_grade = db.query(func.avg(Student.grade)).filter(Student.faculty == faculty).scalar()
    db.close()
    return avg_grade

# Получение списка студентов с оценкой ниже 30 на выбранном курсе
def get_students_below_30_by_course(course: str):
    db = SessionLocal()
    students = db.query(Student).filter(Student.course == course, Student.grade < 30).all()
    db.close()
    return students

if __name__ == "__main__":
    # Инициализация базы данных
    init_db()

    # Заполнение базы данных из CSV
    populate_db_from_csv("students.csv")

    # Пример использования методов
    print("\nСтуденты факультета 'АВТФ':")
    for student in format_students(get_students_by_faculty("АВТФ")):
        print(f"  - {student}")

    print("\nУникальные курсы:")
    for course in get_unique_courses():
        print(f"  - {course}")

    print("\nСредний балл по факультету 'ФПМИ':", get_average_grade_by_faculty("ФПМИ"))

    print("\nСтуденты с оценкой ниже 30 на курсе 'Мат. Анализ':")
    for student in format_students(get_students_below_30_by_course("Мат. Анализ")):
        print(f"  - {student}")