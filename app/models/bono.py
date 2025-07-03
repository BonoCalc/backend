from sqlalchemy import Column, Integer, BigInteger, String, Date, ForeignKey, Float
from app.models.user import Base
from sqlalchemy.orm import relationship
import datetime


class Bono(Base):
    __tablename__ = "bono"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    moneda = Column(String(10), nullable=False)  # Especifica longitud máxima
    valor_nominal = Column(BigInteger, nullable=False)
    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    frecuencia_pago = Column(String(50), nullable=False)  # Especifica longitud
    tipo_tasa = Column(String(50))  # Especifica longitud
    valor_tasa = Column(Float, nullable=False)
    capitalizacion = Column(Integer)
    dias_base = Column(Integer)
    prima_redencion = Column(Float)
    gracia_total_inicio = Column(Integer)
    gracia_total_fin = Column(Integer)
    gracia_parcial_inicio = Column(Integer)
    gracia_parcial_fin = Column(Integer)
    created_at = Column(Date, default=datetime.date.today)
    updated_at = Column(Date, default=datetime.date.today)
    
    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="bonos")
