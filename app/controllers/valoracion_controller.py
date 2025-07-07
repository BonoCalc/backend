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


def calcular_TIR(flujos: list[float]) -> float:
    print("👉 TIR: flujos =", flujos)
    if all(f >= 0 for f in flujos) or all(f <= 0 for f in flujos):
        raise ValueError(
            "Todos los flujos tienen el mismo signo. No se puede calcular TIR."
        )
    tir = npf.irr(flujos)
    if tir is None or math.isnan(tir):
        raise ValueError("No se pudo calcular TIR con numpy-financial")
    return tir

async def valorar_bono(
    bono_id: int, data: ValoracionRequest, db: AsyncSession
) -> ValoracionResponse:
    stmt = select(Bono).where(Bono.id == bono_id)
    result = await db.execute(stmt)
    bono = result.scalar()
    if not bono:
        raise HTTPException(status_code=404, detail="Bono no encontrado")

    stmt = (
        select(FlujoCaja)
        .where(FlujoCaja.bono_id == bono_id)
        .order_by(FlujoCaja.numero_cuota)
    )
    result = await db.execute(stmt)
    flujos = result.scalars().all()
    if not flujos:
        raise HTTPException(status_code=400, detail="El bono no tiene flujos generados")

    flujos_emisor = [-bono.valor_nominal] + [-float(f.cuota) for f in flujos]
    flujos_inversionista = [
        -(data.valor_base if data.origen_valoracion == "PRECIO" else bono.valor_nominal)
    ] + [float(f.cuota) for f in flujos]

    print("Flujos emisor:", flujos_emisor)
    print("Flujos inversionista:", flujos_inversionista)

    if data.origen_valoracion == "TASA":
        p = {"anual": 1, "semestral": 2, "trimestral": 4, "cuatrimestral": 3, "bimestral": 6, "mensual": 12}.get(
            bono.frecuencia_pago.lower(), 1
        )
        tir_inversionista = tir_emisor = data.valor_base / 100 / p
        tir_calculada = None
        precio = bono.valor_nominal
    else:
        try:
            tir_inversionista = calcular_TIR(flujos_inversionista)
            try:
                tir_emisor = calcular_TIR(flujos_emisor)
            except Exception:
                tir_emisor = tir_inversionista 
            tir_calculada = tir_inversionista
            precio = data.valor_base
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"No se pudo calcular la TIR: {str(e)}"
            )

    p = {"anual": 1, "semestral": 2, "trimestral": 4, "cuatrimestral": 3, "bimestral": 6, "mensual": 12}.get(
        bono.frecuencia_pago.lower(), 1
    )
    tcea = (1 + tir_emisor) ** p - 1
    trea = (1 + tir_inversionista) ** p - 1

    y = tir_inversionista
    precio = sum(f.cuota / (1 + y) ** i for i, f in enumerate(flujos, 1))
    pv_tiempo = sum(i * f.cuota / (1 + y) ** i for i, f in enumerate(flujos, 1))
    duracion = pv_tiempo / precio / p
    dur_mod = duracion / (1 + y)
    convexidad = (
        sum(f.cuota * i * (i + 1) / (1 + y) ** (i + 2) for i, f in enumerate(flujos, 1))
        / precio
        / p**2
    )
    precio_maximo = sum(f.cuota for f in flujos)

    valoracion = Valoracion(
        bono_id=bono_id,
        fecha_valoracion=date.today(),
        tcea=round(tcea * 100, 2),
        trea=round(trea * 100, 2),
        duracion=round(duracion, 4),
        duracion_modificada=round(dur_mod, 4),
        convexidad=round(convexidad, 4),
        precio_maximo=round(precio_maximo, 2),
        origen_valoracion=data.origen_valoracion,
        valor_base=data.valor_base,
        precio_calculado=round(precio, 2),
        tir_calculada=round(tir_calculada, 6) if tir_calculada is not None else None,
    )
    db.add(valoracion)
    await db.commit()

    return ValoracionResponse(**valoracion.__dict__)


async def obtener_valoracion_por_bono(
    bono_id: int, db: AsyncSession
) -> ValoracionResponse:
    stmt = select(Bono).where(Bono.id == bono_id)
    result = await db.execute(stmt)
    bono = result.scalar()
    if not bono:
        raise HTTPException(status_code=404, detail="Bono no encontrado")
    stmt = (
        select(Valoracion)
        .where(Valoracion.bono_id == bono_id)
        .order_by(Valoracion.fecha_valoracion.desc())
    )
    result = await db.execute(stmt)
    valoracion = result.scalar()
    
    if not valoracion:
        raise HTTPException(
            status_code=404, 
            detail="No se encontró ninguna valoración para este bono"
        )
    
    return ValoracionResponse(**valoracion.__dict__)
