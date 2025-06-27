from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.bono import Bono
from app.models.valoracion import Valoracion
from app.schemas.valoracion import ValoracionRequest, ValoracionResponse
from app.controllers.flujo_controller import generar_flujos
from datetime import date
import math
from typing import Literal


def calcular_TIR(flujos: list[float], max_iter=100, tol=1e-7) -> float:
    r = 0.05  # Valor inicial
    for _ in range(max_iter):
        f = sum(cf / (1 + r) ** i for i, cf in enumerate(flujos))
        df = sum(-i * cf / (1 + r) ** (i + 1) for i, cf in enumerate(flujos))
        if abs(df) < 1e-10:
            break
        r -= f / df
        if abs(f) < tol:
            return r
    raise ValueError("No converge la TIR")


async def valorar_bono(
    bono_id: int, data: ValoracionRequest, db: AsyncSession
) -> ValoracionResponse:
    stmt = select(Bono).where(Bono.id == bono_id)
    result = await db.execute(stmt)
    bono = result.scalar()

    if not bono:
        raise HTTPException(status_code=404, detail="Bono no encontrado")

    flujos = await generar_flujos(bono_id, db)

    # Flujos desde el emisor (negativos)
    flujos_emisor = [-bono.valor_nominal] + [-f.cuota for f in flujos]
    flujos_inversionista = [
        -(data.valor_base if data.origen_valoracion == "PRECIO" else bono.valor_nominal)
    ] + [f.cuota for f in flujos]

    # TCEA y TREA
    if data.origen_valoracion == "TASA":
        tir_emisor = (1 + data.valor_base / 100) ** (1 / len(flujos)) - 1
        tir_inversionista = tir_emisor
        precio = bono.valor_nominal
        tir_calculada = None
    else:  # PRECIO
        try:
            tir_emisor = calcular_TIR(flujos_emisor)
            tir_inversionista = calcular_TIR(flujos_inversionista)
            tir_calculada = tir_inversionista
        except Exception:
            raise HTTPException(status_code=400, detail="No se pudo calcular TIR")
        precio = data.valor_base

    p = {"anual": 1, "semestral": 2, "trimestral": 4, "mensual": 12}.get(
        bono.frecuencia_pago.lower(), 1
    )
    tcea = (1 + tir_emisor) ** p - 1
    trea = (1 + tir_inversionista) ** p - 1

    # Duración y Convexidad
    y = tir_inversionista
    price = sum(cf.cuota / (1 + y) ** i for i, cf in enumerate(flujos, 1))
    pv_tiempo = sum(i * cf.cuota / (1 + y) ** i for i, cf in enumerate(flujos, 1))
    duracion = pv_tiempo / price / p
    dur_mod = duracion / (1 + y)

    convexidad = (
        sum(
            cf.cuota * i * (i + 1) / (1 + y) ** (i + 2)
            for i, cf in enumerate(flujos, 1)
        )
        / price
    )
    convexidad /= p**2

    # Precio máximo
    precio_maximo = sum(cf.cuota for cf in flujos)

    # Guardar en la DB
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
        tir_calculada=round(tir_calculada, 6) if tir_calculada else None,
    )
    db.add(valoracion)
    await db.commit()

    return ValoracionResponse(**valoracion.__dict__)
