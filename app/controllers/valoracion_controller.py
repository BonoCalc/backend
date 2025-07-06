from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.bono import Bono
from app.models.flujo_caja import FlujoCaja
from app.models.valoracion import Valoracion
from app.schemas.valoracion import ValoracionRequest, ValoracionResponse
from app.controllers.flujo_controller import generar_flujos
from datetime import date
import math
from typing import Literal
import numpy_financial as npf

async def save_valoracion_bono(
    data: ValoracionRequest,
    db: AsyncSession,
    bono_id: int,    
):
    valoracion=Valoracion(
            origen_valoracion=data.origen_valoracion,
            valor_base=data.valor_base,
            bono_id=bono_id
        )
    db.add(valoracion)
    await db.commit()
    await db.refresh(valoracion)
    return valoracion

async def get_valoracion_bono(
    db: AsyncSession,
    bono_id: int,
) -> ValoracionResponse:
    stmt = select(Valoracion).where(Valoracion.bono_id == bono_id)
    result = await db.execute(stmt)
    valoracion = result.scalar_one_or_none()

    if not valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")

    return ValoracionResponse(
        origen_valoracion=valoracion.origen_valoracion,
        valor_base=valoracion.valor_base,
        # Otros campos pueden ser añadidos aquí si es necesario
    )
    
async def edit_valoracion_bono(
    data: ValoracionRequest,
    db: AsyncSession,
    bono_id: int,
) -> ValoracionResponse:
    stmt = select(Valoracion).where(Valoracion.bono_id == bono_id)
    result = await db.execute(stmt)
    valoracion = result.scalar_one_or_none()

    if not valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")

    valoracion.origen_valoracion = data.origen_valoracion
    valoracion.valor_base = data.valor_base

    db.add(valoracion)
    await db.commit()
    await db.refresh(valoracion)

    return ValoracionResponse(
        origen_valoracion=valoracion.origen_valoracion,
        valor_base=valoracion.valor_base,
        # Otros campos pueden ser añadidos aquí si es necesario
    )
