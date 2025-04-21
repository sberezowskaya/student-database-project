from sqlalchemy import Column, Integer, String, Float
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    faculty = Column(String)
    course = Column(String)  # Изменено на String, так как названия курсов текстовые
    grade = Column(Float)

    # Метод для красивого вывода объекта
    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', faculty='{self.faculty}', course='{self.course}', grade={self.grade})"