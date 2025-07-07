from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.core.security import get_current_user_id
from app.schemas.valoracion import ValoracionRequest, ValoracionResponse
from app.controllers.valoracion_controller import valorar_bono, obtener_valoracion_por_bono
from app.controllers.export_controller import exportar_excel
from fastapi.responses import StreamingResponse


router = APIRouter()


@router.post("/{bono_id}/valoracion", response_model=ValoracionResponse)
async def valorar(
    bono_id: int,
    data: ValoracionRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await valorar_bono(bono_id, data, db)


@router.get("/{bono_id}/valoracion/export", response_class=StreamingResponse)
async def exportar_excel_valoracion(
    bono_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await exportar_excel(bono_id, db)


@router.get("/{bono_id}/valoracion", response_model=ValoracionResponse)
async def obtener_valoracion(
    bono_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    Obtiene la valoración más reciente de un bono por su ID.
    """
    return await obtener_valoracion_por_bono(bono_id, db)
