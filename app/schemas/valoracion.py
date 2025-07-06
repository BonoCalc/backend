from pydantic import BaseModel
from typing import Literal
from datetime import date


class ValoracionRequest(BaseModel):
    origen_valoracion: str
    valor_base: float


class ValoracionResponse(BaseModel):
    id: int
    origen_valoracion: str
    valor_base: float
    bono_id: int    
    
    # Agregar configuración para trabajar con modelos SQLAlchemy
    class Config:
        from_attributes = True
