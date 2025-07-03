from pydantic import BaseModel
from datetime import date
from typing import Optional


class BonoCreate(BaseModel):
    moneda: str
    valor_nominal: int
    fecha_emision: date
    fecha_vencimiento: date
    frecuencia_pago: str
    tipo_tasa: str
    valor_tasa: float
    capitalizacion: Optional[int] = None
    dias_base: int
    prima_redencion: Optional[float] = None
    gracia_total_inicio: Optional[int] = None
    gracia_total_fin: Optional[int] = None
    gracia_parcial_inicio: Optional[int] = None
    gracia_parcial_fin: Optional[int] = None


class BonoResponse(BaseModel):
    id: int
    moneda: str
    valor_nominal: int
    fecha_emision: date
    fecha_vencimiento: date
    frecuencia_pago: str
