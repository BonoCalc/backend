from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.core.security import get_current_user_id
from app.schemas.valoracion import ValoracionRequest, ValoracionResponse
from app.controllers.valoracion_controller import (
    save_valoracion_bono,  # ✅ Función que sí existe
    get_valoracion_bono,   # ✅ Función que sí existe
    edit_valoracion_bono,  # ✅ Si la agregaste
)

from app.controllers.export_controller import exportar_excel
from fastapi.responses import StreamingResponse


router = APIRouter()


@router.post("/{bono_id}", response_model=ValoracionResponse)
async def crear_valoracion(
    bono_id: int,
    data: ValoracionRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await save_valoracion_bono(data, db, bono_id)

@router.get("/{bono_id}", response_model=ValoracionResponse)
async def obtener_valoracion(
    bono_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await get_valoracion_bono(db, bono_id)

@router.put("/{bono_id}", response_model=ValoracionResponse)
async def actualizar_valoracion(
    bono_id: int,
    data: ValoracionRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await edit_valoracion_bono(data, db, bono_id)
