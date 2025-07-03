from pydantic import BaseModel

class ConfiguracionSchema(BaseModel):
    moneda_default: str
    tipo_tasa_default: str
    capitalizacion_default: str
    
    
