from pydantic import BaseModel
from datetime import date


class FlujoCajaResponse(BaseModel):
    numero_cuota: int
    fecha: date
    amortizacion: float
    interes: float
    cuota: float
    saldo: float
