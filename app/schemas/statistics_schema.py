from asyncpg.pgproto.pgproto import timedelta
from pydantic import BaseModel
from typing import List, Dict


class InvitationStatistics(BaseModel):
    """Модель для динамики приглашений"""
    date: str
    count: int


class CandidatesStatistics(BaseModel):
    """Модель для статистики по кандидатам"""
    total: int
    last_day: int
    last_week: int
    last_month: int
    hired: int


class CandidatesByAgeStatistics(BaseModel):
    """Модель для распределения кандидатов по возрастным категориям"""
    under_20: int
    between_20_and_30: int
    over_30: int


class CourseStatistics(BaseModel):
    """Модель для статистики по курсам"""
    id: int
    name: str
    candidates: int


class ActivityStatistics(BaseModel):
    """Модель для общей активности"""
    invitation_trend: List[InvitationStatistics]


class Office(BaseModel):
    """Модель для информации об офисе"""
    id: int
    name: str
    location: str


class Manager(BaseModel):
    """Модель для информации о менеджере"""
    full_name: str
    quotas: int
    office_id: Office


class OfficeLoadStatistics(BaseModel):
    """Модель для загрузки офиса"""
    total_candidates: int
    quotas: int
    available_slots: int


class StatisticsResponse(BaseModel):
    """Модель для основного ответа"""
    manager: Manager
    statistics: Dict[str, dict]
