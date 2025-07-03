from app.models.bono import Bono
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.bono import BonoCreate
from fastapi import HTTPException
import datetime


async def create_bono(data: BonoCreate, user_id: int, db: AsyncSession):
    bono = Bono(
        usuario_id=user_id,
        moneda=data.moneda,
        valor_nominal=data.valor_nominal,
        fecha_emision=data.fecha_emision,
        fecha_vencimiento=data.fecha_vencimiento,
        frecuencia_pago=data.frecuencia_pago,
        tipo_tasa=data.tipo_tasa,
        valor_tasa=data.valor_tasa,
        capitalizacion=data.capitalizacion,
        dias_base=data.dias_base,
        prima_redencion=data.prima_redencion,
        gracia_total_inicio=data.gracia_total_inicio,
        gracia_total_fin=data.gracia_total_fin,
        gracia_parcial_inicio=data.gracia_parcial_inicio,
        gracia_parcial_fin=data.gracia_parcial_fin,
    )
    db.add(bono)
    await db.commit()
    await db.refresh(bono)
    return bono


async def list_bonos(user_id: int, db: AsyncSession, limit: int = 10, offset: int = 0):
    stmt = select(Bono).where(Bono.usuario_id == user_id).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()
