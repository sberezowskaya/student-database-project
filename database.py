from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Настройка подключения к базе данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Методы для работы с базой данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_student(db, student_id, name=None, faculty=None, course=None, grade=None):
    """Обновление данных студента."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None
    if name is not None:
        student.name = name
    if faculty is not None:
        student.faculty = faculty
    if course is not None:
        student.course = course
    if grade is not None:
        student.grade = grade
    db.commit()
    db.refresh(student)
    return student

def delete_student(db, student_id):
    """Удаление студента."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None
    db.delete(student)
    db.commit()
    return True