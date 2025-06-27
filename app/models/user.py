from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(255), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)
    created_at = Column(Date, default=datetime.date.today)
