
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.crud.manager_crud import (
    read_manager_by_id,
    read_available_candidates,
    read_candidates_by_manager_id,
)
from app.schemas.manager_schema import getManager

manager_router = APIRouter(
    prefix="/manager",
    tags=["Работа с руководителем"],
)


@manager_router.get("/")
async def get_manager(session: AsyncSession = Depends(get_session)) -> getManager:
    manager = await read_manager_by_id(1, session)
    if manager:
        return getManager.model_validate(manager)
    raise HTTPException(status_code=404, detail="Руководитель не найден")


@manager_router.get("/candidates/")
async def get_candidates(manager_id: int, session: AsyncSession = Depends(get_session)):
    candidates = await read_candidates_by_manager_id(manager_id, session)
    return candidates


@manager_router.get("/candidates/available/")
async def get_available_candidates(session: AsyncSession = Depends(get_session)):
    candidates = await read_available_candidates(session)
    return candidates
