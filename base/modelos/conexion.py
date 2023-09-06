from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime

from base.bd import Base

class Conexion(Base):
    __tablename__ = "conexion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_conexion = Column(DateTime(), default=datetime.now())    
    access_token = Column(String(200), nullable=True)
    refresh_token = Column(String(200), nullable=True)
