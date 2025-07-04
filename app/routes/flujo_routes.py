from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.flujo import FlujoCajaResponse
from app.controllers.flujo_controller import generar_flujos, obtener_flujos_guardados
from app.core.security import get_current_user_id

router = APIRouter()


@router.post("/{bono_id}/flujos", response_model=list[FlujoCajaResponse])
async def obtener_flujos(
    bono_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await generar_flujos(bono_id, db)


@router.get("/{bono_id}/flujos", response_model=list[FlujoCajaResponse])
async def obtener_flujos_route(
    bono_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await obtener_flujos_guardados(bono_id, db)
