from pydantic import BaseModel
from typing import Literal
from datetime import date


class ValoracionRequest(BaseModel):
    origen_valoracion: Literal["TASA", "PRECIO"]
    valor_base: float


class ValoracionResponse(BaseModel):
    fecha_valoracion: date
    tcea: float
    trea: float
    duracion: float
    duracion_modificada: float
    convexidad: float
    precio_maximo: float
    precio_calculado: float
    tir_calculada: float | None
