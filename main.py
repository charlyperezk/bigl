from sqlalchemy.orm import sessionmaker

from base.bd import motor, Base
from base.cliente import ClienteBaseDeDatos
from etl.etl import ETL

import sys
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def crear_base(eliminar_existente: bool) -> None:
    if eliminar_existente:
        Base.metadata.drop_all(motor)
        logging.warning("Todos los datos almacenados en la base de datos han sido eliminados.")
    Base.metadata.create_all(motor, checkfirst=True)
    logging.info("Se ha creado una nueva base de datos")

sesion = sessionmaker(motor)()
cliente = ClienteBaseDeDatos(sesion=sesion)
etl = ETL(cliente_bd=cliente)

def menu() -> None:
    print("")
    print(" Menú: ")
    print(" 1- Configuración inicial ")
    print(" 2- Realizar consulta ")
    print("")
    seleccion_menu = int(input(" Indique la opción deseada: "))
    if seleccion_menu == 1:
        print(" Para comenzar debe crear una base de datos ")
        seleccion_crear_base = int(input(" Desea crear una base de datos? 1 = Si - 0 = No -- "))
        if seleccion_crear_base == 1:
            crear_base(eliminar_existente=False)
        elif seleccion_crear_base == 0:
            print(" Ha indicado que no desea crear una base de datos. ")
            print("")
            menu()
    elif seleccion_menu == 2:
        etl.consultas_disponibles()
        seleccion_usuario = int(input(" Indique la consulta que desea realizar: ... "))
        if seleccion_usuario == 1:
            # lat1 = input(" Indique la latitud del primer punto: ")
            # lat2 = input(" Indique la longitud del primer punto: ")
            # long1 = input(" Indique la latitud del segundo punto: ")
            # long2 = input(" Indique la longitud del segundo punto: ")
            lat1 = "-34.72463539716066"
            lat2 = "-34.71944314591529"
            long1 = "-58.267743699136176"
            long2 = "-58.25844635536899"
            etl.consulta_inmuebles(lat1=lat1, lat2=lat2, long1=long1, long2=long2)

if __name__ == "__main__":
    menu()