import enum
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base


# Статусы для кандидатов
class CandidateStatus(enum.Enum):
    available = "available"
    invited = "invited"
    hired = "hired"


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
    full_name = Column(String(100))
    password = Column(String(100))


# Администратор
class Admin(BaseUser):
    __tablename__ = "admins"


# Руководитель
class Manager(BaseUser):
    __tablename__ = "managers"

    quotas = Column(Integer)
    office_id = Column(Integer, ForeignKey("offices.id"))

    candidates = relationship("Candidate", back_populates="manager")
    quotas_stats = relationship("QuotasStat", back_populates="manager")
    office = relationship("Office", back_populates="managers")


# Кандидат
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, ForeignKey("managers.id"))
    full_name = Column(String(100))
    resume = Column(Text())
    email = Column(String(100), unique=True)
    phone = Column(String(100), unique=True)
    status = Column(
        Enum(CandidateStatus), default=CandidateStatus.available, nullable=False
    )

    manager = relationship("Manager", back_populates="candidates")
    quotas_stats = relationship("QuotasStat", back_populates="candidate")


# Офис
class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    location = Column(String(100))

    managers = relationship("Manager", back_populates="office")


# Статистика
class QuotasStat(Base):
    __tablename__ = "quotas_stat"

    id = Column(Integer, primary_key=True)
    done_by = Column(Integer, ForeignKey("managers.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    old_type = Column(
        Enum(CandidateStatus), default=CandidateStatus.available, nullable=False
    )
    new_type = Column(
        Enum(CandidateStatus), default=CandidateStatus.invited, nullable=False
    )

    manager = relationship("Manager", back_populates="quotas_stats")
    candidate = relationship("Candidate", back_populates="quotas_stats")
