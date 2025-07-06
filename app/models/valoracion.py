from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from app.models.user import Base
from datetime import date
from sqlalchemy.orm import relationship


class Valoracion(Base):
    __tablename__ = "valoraciones"

    id = Column(Integer, primary_key=True)    
    origen_valoracion = Column(String(10))  # "TASA" o "PRECIO"
    valor_base = Column(Float)    
    bono_id = Column(Integer, ForeignKey("bono.id"))
    
    # Agregar relación con Bono
    bono = relationship("Bono", back_populates="valoraciones")
