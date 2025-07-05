from pydantic import BaseModel, Field
from datetime import date


class FlujoCajaResponse(BaseModel):
    numero_cuota: int
    fecha: date
    amortizacion: float
    interes: float
    cuota: float
    saldo: float


class FrecuenciaRequest(BaseModel):
    meses_entre_pagos: int = Field(
        gt=0,
        le=60,
        description="Número de meses entre pagos (por ejemplo, 1, 3, 5, etc.)",
    )
