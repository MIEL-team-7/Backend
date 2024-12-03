from datetime import datetime

from pydantic import BaseModel


class getManager(BaseModel):
    """Модель для сериализации руководителя"""

    id: int
    email: str
    full_name: str
    quotas: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


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
