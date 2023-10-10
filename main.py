import logging
from sqlalchemy.orm import sessionmaker
from base.bd import motor, Base
from base.cliente import ClienteBaseDeDatos
from etl.etl import ETL
from meli.filtro import Filtros
import sys

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

            try:
                seleccion_menu = int(seleccion_menu)
                if seleccion_menu == 1:
                    self.configuracion_inicial()
                elif seleccion_menu == 2:
                    self.realizar_consulta()
                    self.filtro._reiniciar_filtros()
                elif seleccion_menu == 3:
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
            except ValueError:
                print("Entrada no válida. Debe ingresar un número entero.")

    def configuracion_inicial(self):
        print("Para comenzar debe crear una base de datos.")
        seleccion_crear_base = input("¿Desea crear una base de datos? (1 = Si - 0 = No): ")

        try:
            seleccion_crear_base = int(seleccion_crear_base)
            if seleccion_crear_base == 1:
                self.crear_base(eliminar_existente=False)
                print("\nSe ha creado una nueva base de datos.\n")
            elif seleccion_crear_base == 0:
                print("Ha indicado que no desea crear una base de datos.")
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError:
            print("Entrada no válida. Debe ingresar un número entero.")

    def crear_base(self, eliminar_existente: bool) -> None:
        try:
            if eliminar_existente:
                Base.metadata.drop_all(motor)
                logging.warning("Todos los datos almacenados en la base de datos han sido eliminados.")
            Base.metadata.create_all(motor, checkfirst=True)
            logging.info("Se ha creado una nueva base de datos")
        except Exception as e:
            print(f"Error al crear la base de datos: {str(e)}")

    def realizar_consulta(self):
        print("")

        while True:
            filtros = self.filtro._filtros(mostrar=True)
            seleccion = input("Seleccione el filtro deseado (0 = Atrás): ")

            try:
                seleccion = int(seleccion)
                if seleccion == 0:
                    break
                elif seleccion < 1 or seleccion > len(filtros):
                    print("Opción no válida. Intente de nuevo.")
                    continue

                filtro_seleccionado = filtros[seleccion - 1]
                opciones_filtro = self.filtro._opciones(nombre_filtro=filtro_seleccionado, mostrar=True)

                opcion_seleccionada = input("Seleccione la opción de filtrado deseada: ")

                try:
                    opcion_seleccionada = int(opcion_seleccionada)
                    if opcion_seleccionada < 1 or opcion_seleccionada > len(opciones_filtro):
                        print("Opción no válida. Intente de nuevo.")
                        continue

                    opcion_seleccionada -= 1

                    self.filtro._seleccionar_filtro(filtro_seleccionado=(filtro_seleccionado, opcion_seleccionada))

                    print(f"Filtro '{filtro_seleccionado}' seleccionado con la opción '{opcion_seleccionada}'")
                    usuario_ag_filtro = input("¿Desea agregar otro filtro? (1 = Si - 0 = No): ")

                    if usuario_ag_filtro != "1":
                        # self.filtro._seleccion(mostrar=True)
                        print("")
                        self.etl.consulta()
                        self.filtro.filtros_aplicados.clear()
                        break
                except ValueError:
                    print("Entrada no válida. Debe ingresar un número entero.")
                except Exception as e:
                    logging.error(f"Error no manejado hizo caer el programa. Mensaje {e}")
                    raise RuntimeError("Error no manejado hizo caer el programa")
            except ValueError:
                print("Entrada no válida. Debe ingresar un número entero.")

    def seleccion_filtros(self):
        filtros = self.filtro._filtros(mostrar=True)
        seleccion = input("Seleccione el filtro deseado: ")

        try:
            seleccion = int(seleccion)
            if seleccion < 1 or seleccion > len(filtros):
                print("Opción no válida. Intente de nuevo.")
                return
        except ValueError:
            print("Entrada no válida. Debe ingresar un número entero.")
            return

        self.filtro._opciones(nombre_filtro=filtros[seleccion - 1], mostrar=True)
        opcion_seleccionada = input("Seleccione la opción de filtrado deseada (si desea volver hacia atrás coloque 0): ")

        try:
            opcion_seleccionada = int(opcion_seleccionada)
            self.filtro._seleccionar_filtro(nombre_filtro=filtros[seleccion - 1], opcion=opcion_seleccionada)
        except ValueError:
            print("Entrada no válida. Debe ingresar un número entero.")

if __name__ == "__main__":
    menu = Menu()
    print("")
    print("¡Bienvenido a Bigl!")
    menu.mostrar()
