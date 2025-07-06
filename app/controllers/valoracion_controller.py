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
    # Verificar que el bono existe
    stmt = select(Bono).where(Bono.id == bono_id)
    result = await db.execute(stmt)
    bono = result.scalar_one_or_none()
    
    if not bono:
        raise HTTPException(status_code=404, detail="Bono no encontrado")
    
    # Verificar si ya existe una valoración para este bono
    stmt = select(Valoracion).where(Valoracion.bono_id == bono_id)
    result = await db.execute(stmt)
    existing_valoracion = result.scalar_one_or_none()
    
    if existing_valoracion:
        raise HTTPException(
            status_code=409, 
            detail="Ya existe una valoración para este bono"
        )
    
    valoracion = Valoracion(
        origen_valoracion=data.origen_valoracion,
        valor_base=data.valor_base,
        fecha_valoracion=data.fecha_valoracion,
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
        id=valoracion.id,
        origen_valoracion=valoracion.origen_valoracion,
        valor_base=valoracion.valor_base,
        fecha_valoracion=valoracion.fecha_valoracion,
        bono_id=valoracion.bono_id
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

    await db.commit()
    await db.refresh(valoracion)

    return ValoracionResponse(
        id=valoracion.id,
        origen_valoracion=valoracion.origen_valoracion,
        valor_base=valoracion.valor_base,
        fecha_valoracion=valoracion.fecha_valoracion,
        bono_id=valoracion.bono_id
    )