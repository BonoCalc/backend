from app.models.bono import Bono
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.schemas.bono import BonoCreate, BonoUpdate
from fastapi import HTTPException
from app.schemas.bono import BonoResponse
from app.models.flujo_caja import FlujoCaja
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


async def get_bono_by_id(bono_id: int, user_id: int, db: AsyncSession) -> BonoResponse:
    result = await db.execute(
        select(Bono).where(Bono.id == bono_id, Bono.usuario_id == user_id)
    )
    bono = result.scalar()
    if not bono:
        raise HTTPException(status_code=404, detail="Bono no encontrado")
    return BonoResponse(**bono.__dict__)


async def update_bono(
    bono_id: int, user_id: int, data: BonoUpdate, db: AsyncSession
) -> BonoResponse:
    result = await db.execute(
        select(Bono).where(Bono.id == bono_id, Bono.usuario_id == user_id)
    )
    bono = result.scalar()

    if not bono:
        raise HTTPException(status_code=404, detail="Bono no encontrado")

    # Solo actualiza campos presentes
    for field, value in data.dict(exclude_unset=True).items():
        setattr(bono, field, value)

    await db.execute(delete(FlujoCaja).where(FlujoCaja.bono_id == bono.id))
    await db.commit()
    await db.refresh(bono)
    return BonoResponse(**bono.__dict__)
