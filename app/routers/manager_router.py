from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from crud.manager_crud import (
    read_manager_by_id,
    read_available_candidates,
    read_candidates_by_manager_id,
)
from schemas.manager_schema import getManager

manager_router = APIRouter(
    prefix="/manager",
    tags=["Работа с руководителем"],
)


@manager_router.get("/{id}", response_model=getManager)
async def get_manager(id: int, session: AsyncSession = Depends(get_session)):
    manager = await read_manager_by_id(id, session)
    if manager:
        return manager
    raise HTTPException(status_code=404, detail="Руководитель не найден")


@manager_router.get("/candidates/")
async def get_candidates(manager_id: int, session: AsyncSession = Depends(get_session)):
    candidates = await read_candidates_by_manager_id(manager_id, session)
    return candidates


@manager_router.get("/candidates/available/")
async def get_available_candidates(session: AsyncSession = Depends(get_session)):
    candidates = await read_available_candidates(session)
    return candidates
