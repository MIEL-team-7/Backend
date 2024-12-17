from datetime import date

from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.manager_crud import read_manager_by_id
from app.crud.statistics_crud import (
    get_candidate_count,
    get_available_candidates,
    get_candidate_filter_date,
    get_available_candidates_count,
    get_candidate_statistics, get_office_load_statistics, )
from app.schemas.statistics_schema import (
    StatisticsResponse,
    Manager,
    Office,
    CandidatesStatistics,
    OfficeLoadStatistics,
    CandidatesByAgeStatistics,
    CourseStatistics,
    ActivityStatistics,
    InvitationStatistics,
)
from app.core.db import get_session

statistics = APIRouter(
    prefix="/statistics",
    tags=["Работа со статистикой"]
)


@statistics.get("/{manager_id}", response_model=StatisticsResponse)
async def get_statistics(manager_id: int, session: AsyncSession = Depends(get_session)):
    # Пример данных (заполните данными из базы)
    manager_data = await read_manager_by_id(manager_id, session)

    statistics_data = {
        "candidates": get_candidate_statistics(),
    }

    return StatisticsResponse(manager=manager_data, statistics=statistics_data)
