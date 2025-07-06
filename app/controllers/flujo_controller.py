from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models.bono import Bono
from app.schemas.flujo import FlujoCajaResponse
from app.models.flujo_caja import FlujoCaja
from datetime import date
from dateutil.relativedelta import relativedelta


def calcular_periodos(bono: Bono) -> int:
    dias = (bono.fecha_vencimiento - bono.fecha_emision).days
    base = bono.dias_base or 360
    pagos_por_anio = {"anual": 1, "semestral": 2, "trimestral": 4, "cuatrimestral": 3, "bimestral": 6, "mensual": 12}
    frecuencia = pagos_por_anio.get(bono.frecuencia_pago.lower(), 1)
    return int(frecuencia * (dias / base))


async def generar_flujos(
    bono_id: int, meses_entre_pagos: int, db: AsyncSession
) -> list[FlujoCajaResponse]:
    stmt = select(Bono).where(Bono.id == bono_id)
    result = await db.execute(stmt)
    bono = result.scalar()

    if not bono:
        raise HTTPException(status_code=404, detail="Bono no encontrado")

    await db.execute(delete(FlujoCaja).where(FlujoCaja.bono_id == bono.id))

    fecha_ini = bono.fecha_emision
    fecha_fin = bono.fecha_vencimiento
    n = 0
    fecha = fecha_ini
    while fecha < fecha_fin:
        fecha += relativedelta(months=meses_entre_pagos)
        n += 1

    p = 12 / meses_entre_pagos  
    if bono.tipo_tasa.lower() == "efectiva":
        i = (1 + bono.valor_tasa / 100) ** (1 / p) - 1
    else:
        tna = bono.valor_tasa / 100
        i = tna / p

    amort = (
        bono.valor_nominal / (n - (bono.gracia_total_fin or 0))
        if n != (bono.gracia_total_fin or 0)
        else 0
    )
    
    saldo = bono.valor_nominal
    flujos = []

    for k in range(1, n + 1):
        fecha_pago = bono.fecha_emision + relativedelta(months=k * meses_entre_pagos)
        
        en_gracia_total = (
            bono.gracia_total_inicio
            and bono.gracia_total_inicio <= k <= bono.gracia_total_fin
        )
        en_gracia_parcial = (
            bono.gracia_parcial_inicio
            and bono.gracia_parcial_inicio <= k <= bono.gracia_parcial_fin
        )

        if en_gracia_total:
            interes = 0
            amortizacion = 0
            saldo *= (1 + i)
        elif en_gracia_parcial:
            interes = saldo * i
            amortizacion = 0
        else:
            interes = saldo * i
            amortizacion = amort
            saldo -= amortizacion

        cuota = interes + amortizacion
        
        if k == n and bono.prima_redencion:
            cuota += saldo * (bono.prima_redencion / 100)

        db.add(
            FlujoCaja(
                numero_cuota=k,
                fecha=fecha_pago,
                amortizacion=round(amortizacion, 2),
                interes=round(interes, 2),
                cuota=round(cuota, 2),
                saldo=round(saldo, 2),
                bono_id=bono.id,
            )
        )
        flujos.append(
            FlujoCajaResponse(
                numero_cuota=k,
                fecha=fecha_pago,
                amortizacion=round(amortizacion, 2),
                interes=round(interes, 2),
                cuota=round(cuota, 2),
                saldo=round(saldo, 2),
            )
        )

    await db.commit()
    return flujos


async def obtener_flujos_guardados(
    bono_id: int, db: AsyncSession
) -> list[FlujoCajaResponse]:
    stmt = (
        select(FlujoCaja)
        .where(FlujoCaja.bono_id == bono_id)
        .order_by(FlujoCaja.numero_cuota)
    )
    result = await db.execute(stmt)
    flujos = result.scalars().all()

    return [
        FlujoCajaResponse(
            numero_cuota=f.numero_cuota,
            fecha=f.fecha,
            amortizacion=f.amortizacion,
            interes=f.interes,
            cuota=f.cuota,
            saldo=f.saldo,
        )
        for f in flujos
    ]
