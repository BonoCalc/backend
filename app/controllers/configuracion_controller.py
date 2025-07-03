from app.models.configuracion import Configuracion
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.configuracion import ConfiguracionSchema
from fastapi import HTTPException

async def create_configuracion(
    data: ConfiguracionSchema,
    user_id: int,
    db: AsyncSession
):
    configuracion = Configuracion(
        usuario_id=user_id,
        moneda_default=data.moneda_default,
        tipo_tasa_default=data.tipo_tasa_default,
        capitalizacion_default=data.capitalizacion_default
    )
    db.add(configuracion)
    await db.commit()
    await db.refresh(configuracion)
    return configuracion

async def get_configuracion(
    user_id: int,
    db: AsyncSession
):
    stmt = select(Configuracion).where(Configuracion.usuario_id == user_id)
    result = await db.execute(stmt)
    configuracion = result.scalar_one_or_none()
    
    if not configuracion:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    
    return configuracion

async def update_configuracion(
    user_id: int,
    data: ConfiguracionSchema,
    db: AsyncSession
):
    configuracion = await get_configuracion(user_id, db)
    
    configuracion.moneda_default = data.moneda_default
    configuracion.tipo_tasa_default = data.tipo_tasa_default
    configuracion.capitalizacion_default = data.capitalizacion_default
    
    db.add(configuracion)
    await db.commit()
    await db.refresh(configuracion)
    
    return configuracion