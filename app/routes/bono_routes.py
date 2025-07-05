from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.core.security import get_current_user_id
from app.schemas.bono import BonoCreate, BonoResponse, BonoUpdate
from app.controllers.bono_controller import (
    create_bono,
    list_bonos,
    get_bono_by_id,
    update_bono,
)

router = APIRouter()


@router.post("/", response_model=BonoResponse)
async def registrar_bono(
    data: BonoCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await create_bono(data, user_id, db)


@router.get("/", response_model=list[BonoResponse])
async def listar_bonos(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await list_bonos(user_id, db, limit=limit, offset=offset)


@router.get("/{bono_id}", response_model=BonoResponse)
async def obtener_bono_por_id(
    bono_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await get_bono_by_id(bono_id, user_id, db)


@router.put("/{bono_id}", response_model=BonoResponse)
async def actualizar_bono(
    bono_id: int,
    data: BonoUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await update_bono(bono_id, user_id, data, db)
