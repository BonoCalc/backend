from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.bono import Bono
from app.schemas.flujo import FlujoCajaResponse


def calcular_periodos(bono: Bono) -> int:
    dias = (bono.fecha_vencimiento - bono.fecha_emision).days
    base = bono.dias_base or 360
    pagos_por_anio = {"anual": 1, "semestral": 2, "trimestral": 4, "mensual": 12}
    frecuencia = pagos_por_anio.get(bono.frecuencia_pago.lower(), 1)
    return int(frecuencia * (dias / base))


async def generar_flujos(bono_id: int, db: AsyncSession) -> list[FlujoCajaResponse]:
    stmt = select(Bono).where(Bono.id == bono_id)
    result = await db.execute(stmt)
    bono = result.scalar()

    if not bono:
        raise HTTPException(status_code=404, detail="Bono no encontrado")

    n = calcular_periodos(bono)
    p = {"anual": 1, "semestral": 2, "trimestral": 4, "mensual": 12}.get(
        bono.frecuencia_pago.lower(), 1
    )

    # Calcular tasa por periodo
    if bono.tipo_tasa.lower() == "efectiva":
        i = (1 + bono.valor_tasa / 100) ** (1 / p) - 1
    else:
        m = bono.capitalizacion or 1
        tna = bono.valor_tasa / 100
        i = (1 + tna / m) ** (1 / m) - 1

    saldo = bono.valor_nominal
    amort = (
        bono.valor_nominal / (n - (bono.gracia_total_fin or 0))
        if n != (bono.gracia_total_fin or 0)
        else 0
    )
    flujos = []

    for k in range(1, n + 1):
        fecha_pago = bono.fecha_emision + timedelta(days=(k * 360 // p))
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
            saldo *= 1 + i
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

    return flujos
