from pydantic import BaseModel
from typing import Literal
from datetime import date


class ValoracionRequest(BaseModel):
    origen_valoracion: str
    valor_base: float
    


class ValoracionResponse(BaseModel):
    origen_valoracion: str
    valor_base: float
