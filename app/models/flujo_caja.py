from sqlalchemy import Column, Integer, Date, ForeignKey, Float
from app.models.user import Base
from sqlalchemy.orm import relationship


class FlujoCaja(Base):
    __tablename__ = "flujos_caja"

    id = Column(Integer, primary_key=True)
    numero_cuota = Column(Integer)
    fecha = Column(Date)
    amortizacion = Column(Float)
    interes = Column(Float)
    cuota = Column(Float)
    saldo = Column(Float)
    bono_id = Column(Integer, ForeignKey("bono.id"))
