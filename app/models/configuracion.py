from sqlalchemy import Column, Integer, BigInteger, String, Date, ForeignKey, Float
from app.models.user import Base
from sqlalchemy.orm import relationship


class Configuracion(Base):
    __tablename__ = "configuracion"
    
    # Clave primaria que también es foreign key (relación 1:1)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    moneda_default = Column(String)
    tipo_tasa_default = Column(String)
    capitalizacion_default = Column(String)
    
    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="configuracion")

