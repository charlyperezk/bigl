from sqlalchemy.orm import sessionmaker

from base.bd import motor, Base
from base.cliente import ClienteBaseDeDatos
from etl.etl import ETL
from meli.filtro import Filtros

import sys
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Menu:
    def __init__(self):
        self.sesion = sessionmaker(motor)()
        self.cliente = ClienteBaseDeDatos(sesion=self.sesion)
        self.filtro = Filtros()
        self.etl = ETL(cliente_bd=self.cliente, filtro=self.filtro)

    def mostrar(self):
        while True:
            print("\nMenú:")
            print("1- Configuración inicial")
            print("2- Realizar consulta")
            print("3- Salir")

            seleccion_menu = input("Indique la opción deseada: ")

            if seleccion_menu == "1":
                self.configuracion_inicial()
            elif seleccion_menu == "2":
                self.realizar_consulta()
            elif seleccion_menu == "3":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def configuracion_inicial(self):
        print("Para comenzar debe crear una base de datos.")
        seleccion_crear_base = input(
            "¿Desea crear una base de datos? (1 = Si - 0 = No): ")
        if seleccion_crear_base == "1":
            self.crear_base(eliminar_existente=False)
            print("\nSe ha creado una nueva base de datos.\n")
        elif seleccion_crear_base == "0":
            print("Ha indicado que no desea crear una base de datos.")
        else:
            print("Opción no válida. Intente de nuevo.")

    def crear_base(eliminar_existente: bool) -> None:
        if eliminar_existente:
            Base.metadata.drop_all(motor)
            logging.warning(
                "Todos los datos almacenados en la base de datos han sido eliminados.")
        Base.metadata.create_all(motor, checkfirst=True)
        logging.info("Se ha creado una nueva base de datos")

    def realizar_consulta(self):
        print("")

        while True:
            filtros = self.filtro._filtros(mostrar=True)
            seleccion = input(
                "Seleccione el filtro deseado (0 = Atrás): ")

            if seleccion == "0":
                continue # Salir del bucle si el usuario elige '0'

            if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(filtros):
                print("Opción no válida. Intente de nuevo.")
                continue  # Ignorar opciones inválidas y volver al principio del bucle

            filtro_seleccionado = filtros[int(seleccion) - 1]
            opciones_filtro = self.filtro._opciones(
                nombre_filtro=filtro_seleccionado, mostrar=True)

            opcion_seleccionada = input(
                "Seleccione la opción de filtrado deseada: ")

            if not opcion_seleccionada.isdigit() or int(opcion_seleccionada) < 1 or int(opcion_seleccionada) > len(
                    opciones_filtro):
                print("Opción no válida. Intente de nuevo.")
                continue  # Ignorar opciones inválidas y volver al principio del bucle

            opcion_seleccionada = int(opcion_seleccionada) - 1

            self.filtro._seleccionar_filtro(filtro_seleccionado=(filtro_seleccionado, opcion_seleccionada))

            print(
                f"Filtro '{filtro_seleccionado}' seleccionado con la opción '{opcion_seleccionada}'")
            usuario_ag_filtro = input(
                "¿Desea agregar otro filtro? (1 = Si - 0 = No): ")

            if usuario_ag_filtro != "1":
                self.filtro._seleccion(mostrar=True)
                self.etl.consulta(mostrar=True)
                self.filtro.filtros_aplicados.clear()
                break  # Salir del bucle si el usuario no quiere agregar más filtros

    def seleccion_filtros(self):
        filtros = self.filtro._filtros(mostrar=True)
        seleccion = input("Seleccione el filtro deseado: ")
        self.filtro._opciones(
            nombre_filtro=filtros[int(seleccion) - 1], mostrar=True)
        opcion_seleccionada = input(
            "Seleccione la opción de filtrado deseada (si desea volver hacia atrás coloque 0): ")
        self.filtro._seleccionar_filtro(nombre_filtro=filtros[int(
            seleccion) - 1], opcion=int(opcion_seleccionada))

if __name__ == "__main__":
    menu = Menu()
    menu.mostrar()
