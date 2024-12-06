from datetime import datetime
from typing import List

from pydantic import BaseModel


class getOffice(BaseModel):
    """Модель для сериализации офиса"""

    id: int
    name: str
    location: str

    class Config:
        orm_mode = True


class getSkill(BaseModel):
    """Модель для сериализации навыка"""

    id: int
    name: str

    class Config:
        orm_mode = True


class getManager(BaseModel):
    """Модель для сериализации руководителя"""

    id: int
    email: str
    full_name: str
    quotas: int
    office: getOffice
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class getCandidate(BaseModel):
    """Модель для сериализации кандидата"""

    id: int
    photo: str
    full_name: str
    email: str
    location: str
    resume: str
    phone: str
    is_hired: bool
    clients: int
    objects: int
    skills: List[getSkill] | None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
