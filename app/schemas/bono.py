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
    tipo_tasa: str
    valor_tasa: float
    capitalizacion: Optional[int] = None
    dias_base: int
    prima_redencion: Optional[float] = None
    gracia_total_inicio: Optional[int] = None
    gracia_total_fin: Optional[int] = None
    gracia_parcial_inicio: Optional[int] = None
    gracia_parcial_fin: Optional[int] = None


class BonoUpdate(BaseModel):
    moneda: Optional[str] = None
    valor_nominal: Optional[int] = None
    fecha_emision: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    frecuencia_pago: Optional[str] = None
    tipo_tasa: Optional[str] = None
    valor_tasa: Optional[float] = None
    capitalizacion: Optional[int] = None
    dias_base: Optional[int] = None
    prima_redencion: Optional[int] = None
    gracia_total_inicio: Optional[int] = None
    gracia_total_fin: Optional[int] = None
    gracia_parcial_inicio: Optional[int] = None
    gracia_parcial_fin: Optional[int] = None
