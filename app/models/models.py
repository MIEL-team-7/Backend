from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.db import Base


# Абстрактная модель
class BaseModel(Base):
    __abstract__ = True  # Не создаст таблицу в БД, так как это абстрактная модель

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


# Абстрактная модель пользователя
class BaseUser(BaseModel):
    __abstract__ = True  # Не создаст таблицу в БД, так как это абстрактная модель

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))


# Администратор
class Admin(BaseUser):
    __tablename__ = "admins"

    is_superadmin = Column(Boolean, default=False)


# Руководитель
class Manager(BaseUser):
    __tablename__ = "managers"

    full_name = Column(String(100))
    quotas = Column(Integer, index=True)
    office_id = Column(Integer, ForeignKey("offices.id"))

    candidates = relationship("ManagerCandidate", back_populates="manager")
    office = relationship("Office", back_populates="managers")


# Кандидат
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    photo = Column(String(255))  # Путь к фото
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    location = Column(String(100))
    resume = Column(String(255))  # Путь к резюме
    phone = Column(String(100), unique=True)
    is_hired = Column(Boolean, default=False, index=True)
    clients = Column(Integer, default=0)
    objects = Column(Integer, default=0)

    managers = relationship("ManagerCandidate", back_populates="candidate")
    courses = relationship("CandidateCourse", back_populates="candidate")


# Офис
class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    location = Column(String(100))

    managers = relationship("Manager", back_populates="office")


# Связь между руководителем и кандидатом
class ManagerCandidate(Base):
    __tablename__ = "manager_candidates"

    id = Column(Integer, primary_key=True)
    done_by = Column(Integer, ForeignKey("managers.id"), index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), index=True)
    is_viewed = Column(Boolean, default=True, index=True)

    manager = relationship("Manager", back_populates="candidates")
    candidate = relationship("Candidate", back_populates="managers")


# Курсы кандидата
class CandidateCourse(Base):
    __tablename__ = "candidate_courses"

    id = Column(Integer, primary_key=True)
    course = Column(Integer, ForeignKey("courses.id"), index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), index=True)

    candidate = relationship("Candidate", back_populates="courses")
    course = relationship("Course", back_populates="candidates")


# Курсы
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    candidates = relationship("CandidateCourse", back_populates="course")
