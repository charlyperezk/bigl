import os

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

try:
    motor = create_engine(os.getenv("BASEDATOS_URL"))
except:
    raise Exception("No se ha podido crear la instancia del motor de base de datos. Chequea si la variable de entorno BASEDATOS_URL está definida o es incorrecta.")
Base = declarative_base()
