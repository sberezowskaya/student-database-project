from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db, init_db
from models import Student

# Создание экземпляра FastAPI
app = FastAPI()

# Инициализация базы данных при старте приложения
@app.on_event("startup")
def on_startup():
    init_db()

# Эндпойнт для создания нового студента
@app.post("/students/", response_model=dict)
def create_student(name: str, faculty: str, course: str, grade: float, db: Session = Depends(get_db)):
    """
    Создает нового студента в базе данных.
    """
    new_student = Student(name=name, faculty=faculty, course=course, grade=grade)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Student created", "student": new_student}

# Эндпойнт для получения всех студентов
@app.get("/students/", response_model=list[dict])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Возвращает список студентов с возможностью пагинации.
    """
    students = db.query(Student).offset(skip).limit(limit).all()
    return [{"id": s.id, "name": s.name, "faculty": s.faculty, "course": s.course, "grade": s.grade} for s in students]

# Эндпойнт для получения одного студента по ID
@app.get("/students/{student_id}", response_model=dict)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """
    Возвращает информацию о студенте по его ID.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"id": student.id, "name": student.name, "faculty": student.faculty, "course": student.course, "grade": student.grade}

# Эндпойнт для обновления данных студента
@app.put("/students/{student_id}", response_model=dict)
def update_student_endpoint(
    student_id: int,
    name: str = None,
    faculty: str = None,
    course: str = None,
    grade: float = None,
    db: Session = Depends(get_db),
):
    """
    Обновляет данные студента по его ID.
    """
    updated_student = update_student(db, student_id, name, faculty, course, grade)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated", "student": updated_student}

# Эндпойнт для удаления студента
@app.delete("/students/{student_id}", response_model=dict)
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    """
    Удаляет студента по его ID.
    """
    success = delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}

# Запуск сервера (только для локального использования)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    from fastapi import Depends, HTTPException, status
from auth import get_current_user

# Пример защищенного эндпойнта
@app.get("/students/", response_model=list[dict])
def read_students(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [{"id": s.id, "name": s.name, "faculty": s.faculty, "course": s.course, "grade": s.grade} for s in students]

from fastapi import FastAPI
from auth_router import router as auth_router

app = FastAPI()

# Подключение маршрутизатора /auth
app.include_router(auth_router)