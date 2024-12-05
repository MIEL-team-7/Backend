from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.crud.manager_crud import (
    read_manager_by_id,
    read_available_candidates,
    read_candidates_by_manager_id,
    read_candidate_by_id,
)
from app.schemas.manager_schema import getManager, getCandidate
from app.core.logging import logger

manager_router = APIRouter(
    prefix="/manager",
    tags=["Работа с руководителем"],
)


@manager_router.get(
    "/", response_model=getManager
)  # TODO: После мерджа с авторизацией сделать опредление id по токену
async def get_manager(id: int, session: AsyncSession = Depends(get_session)):
    logger.debug("Запуск роутера /manager/")

    manager = await read_manager_by_id(id, session)
    if manager:
        return manager
    logger.error("Руководитель не найден")
    raise HTTPException(status_code=404, detail="Руководитель не найден")


@manager_router.get(
    "/get_candidates/", response_model=List[getCandidate]
)  # TODO: После мерджа с авторизацией сделать опредление id по токену
async def get_candidates_of_manager(
    manager_id: int, session: AsyncSession = Depends(get_session)
):
    logger.debug("Запуск роутера manager/get_candidates/")

    candidates = await read_candidates_by_manager_id(manager_id, session)
    return candidates


@manager_router.get(
    "/get_available_candidates/", response_model=List[getCandidate]
)  # TODO: После мерджа с авторизацией сделать опредление id по токену
async def get_available_candidates(session: AsyncSession = Depends(get_session)):
    logger.debug("Запуск роутера manager/get_available_candidates/")

    candidates = await read_available_candidates(session)
    return candidates


@manager_router.get(
    "/get_candidate_by_id/", response_model=getCandidate
)  # TODO: После мерджа с авторизацией сделать опредление id по токену
async def get_candidate_by_id(
    candidate_id: int, session: AsyncSession = Depends(get_session)
):
    logger.debug("Запуск роутера manager/get_candidate_by_id/ с id: %s", candidate_id)

    candidate = await read_candidate_by_id(candidate_id, session)
    if candidate:
        return candidate
    logger.error("Кандидат не найден")

    raise HTTPException(status_code=404, detail="Кандидат не найден")
