from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from app.models.user import Base
from datetime import date


class Valoracion(Base):
    __tablename__ = "valoraciones"

    id = Column(Integer, primary_key=True)
    fecha_valoracion = Column(Date, default=date.today)
    tcea = Column(Float)
    trea = Column(Float)
    duracion = Column(Float)
    duracion_modificada = Column(Float)
    convexidad = Column(Float)
    precio_maximo = Column(Float)
    origen_valoracion = Column(String(10))  # "TASA" o "PRECIO"
    valor_base = Column(Float)
    precio_calculado = Column(Float)
    tir_calculada = Column(Float, nullable=True)
    bono_id = Column(Integer, ForeignKey("bono.id"))
