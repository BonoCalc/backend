from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.core.security import get_current_user_id
from app.schemas.configuracion import ConfiguracionSchema
from app.controllers.configuracion_controller import create_configuracion, get_configuracion, update_configuracion

router = APIRouter()

@router.post("/", response_model=ConfiguracionSchema)
async def registrar_configuracion(
    data: ConfiguracionSchema,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await create_configuracion(data, user_id, db)

@router.get("/", response_model=ConfiguracionSchema)
async def obtener_configuracion(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await get_configuracion(user_id, db)

@router.put("/", response_model=ConfiguracionSchema)
async def actualizar_configuracion(
    data: ConfiguracionSchema,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await update_configuracion(user_id, data, db)