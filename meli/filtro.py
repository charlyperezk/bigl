from meli.variables import Variables
from herramientas.excepciones import FiltroError, VariableError
import logging
import json

class Filtros:
    """
    Filtros se encarga del manejo de filtros de búsqueda. Almacena la selección de filtros del usuario.
    Pueden agregarse filtros a través del archivo .env.

    Atributos
    ----------
    filtros_aplicados: list
        Lista que posee los filtros que ha seleccionado el usuario.
    filtros_disponibles: list
        Listado de filtros disponibles (filtros_disponibles en .env).
    """

    filtros_aplicados = []
    filtros_disponibles = json.loads(Variables.traer_variable("FILTROS_DISPONIBLES"))

    @classmethod
    def _filtros(cls, mostrar: bool=False) -> json:
        """
        Obtiene los filtros de búsqueda disponibles desde las variables de entorno.

        Args:
            mostrar (bool): Indica si se deben mostrar los filtros disponibles en la consola.

        Returns:
            json: La lista de filtros disponibles.

        Raises:
            FiltroError: Si ocurre un error al obtener los filtros disponibles.
        """
        try:
            filtros = cls.filtros_disponibles
            if mostrar:
                print(f" Filtros de búsqueda disponibles: ")
                print("")
                for e, filtro_disponible in enumerate(filtros):
                    print(e + 1, "--", filtro_disponible.lower())
                print("")
            return filtros
        except VariableError as e:
            logging.error(f"Variable error - Mensaje: {str(e)}")
        except:
            raise FiltroError("Error al mostrar los filtros disponibles. Estos se encuentran en FILTROS_DISPONIBLES del archivo .env.")

    @classmethod
    def _opciones(cls, nombre_filtro: str, mostrar: bool=False, llaves: bool=False) -> list or dict:
        """
        Obtiene las opciones para un filtro específico.

        Args:
            nombre_filtro (str): El nombre del filtro.
            mostrar (bool): Indica si se deben mostrar las opciones en la consola.
            llaves (bool): Indica si se deben devolver las llaves de las opciones.

        Returns:
            list or dict: La lista de opciones o el diccionario completo de opciones.

        Raises:
            FiltroError: Si el filtro seleccionado no se encuentra en los disponibles.
            VariableError: Si ocurre un error al obtener las opciones del filtro.
        """
        try:
            disponibles = cls._filtros()
            if nombre_filtro not in disponibles:
                raise FiltroError("El filtro seleccionado no se encuentra dentro de los disponibles")
            filtro = Variables.traer_variable(nombre_variable=nombre_filtro)
            filtro = json.loads(filtro)
            opciones = list(filtro.keys())
            if mostrar:
                print(f" Opciones de {nombre_filtro.lower()} son: ")
                print("")
                for e, opcion in enumerate(opciones[1:]):
                    print(e + 1, "--", opcion)
                print("")
            if llaves:
                return opciones[1:]
            else:
                return filtro
        except FiltroError as e:
            logging.error(f"Filtro error - Mensaje: {str(e)}")
        except VariableError as e:
            logging.error(f"Variable error - Mensaje: {str(e)}")
        except:
            raise FiltroError("Error al mostrar las opciones de {nombre_filtro}. Estas se encuentran en el archivo .env.")

    @classmethod
    def _seleccionar_filtro(cls, filtro_seleccionado: tuple) -> None:
        """
        Agrega un filtro seleccionado a la lista de filtros aplicados.

        Args:
            filtro_seleccionado (tuple): Una tupla que contiene el nombre del filtro y la opción seleccionada.

        Raises:
            FiltroError: Si el filtro seleccionado no se encuentra en los disponibles o si hay un error al seleccionar el filtro.
            VariableError: Si hay un error al obtener las opciones del filtro.
        """
        try:
            disponibles = cls._filtros()
            nombre_filtro = filtro_seleccionado[0]
            opcion = filtro_seleccionado[1]
            if nombre_filtro not in disponibles:
                logging.error("Filtro error - El filtro seleccionado no se encuentra dentro de los disponibles")
                raise FiltroError("El filtro seleccionado no se encuentra dentro de los disponibles")
            opciones_filtro = cls._opciones(nombre_filtro=nombre_filtro)
            llaves_opciones = list(cls._opciones(nombre_filtro=nombre_filtro, llaves=True))
            opcion_seleccionada = llaves_opciones[opcion]
            query = opciones_filtro["ID"].lower() + opciones_filtro[opcion_seleccionada]
            cls.filtros_aplicados.append(query)
            for filtro in cls.filtros_disponibles:
                if filtro == nombre_filtro:
                    cls.filtros_disponibles.remove(filtro)
            print("")
            logging.info("Se ha añadido el filtro exitosamente")
        except FiltroError as e:
            logging.error(f"Filtro error - Mensaje: {str(e)}")
        except VariableError as e:
            logging.error(f"Variable error - Mensaje: {str(e)}")

    @classmethod
    def _seleccion(cls, mostrar: bool=False) -> list:
        """
        Obtiene la lista de filtros aplicados.

        Args:
            mostrar (bool): Indica si se deben mostrar los filtros aplicados en la consola.

        Returns:
            list: La lista de filtros aplicados.

        Raises:
            FiltroError: Si hay un error al obtener los filtros aplicados.
        """
        seleccion = cls.filtros_aplicados
        if mostrar:
            logging.info("Consulta iniciada.")
            print("Filtros Aplicados:")
            for filtro in seleccion:
                print((f" - {filtro}"))
        return seleccion

    def _reiniciar_filtros(cls):
        """
        Declara nuevamente el listado de filtros disponibles
        """
        cls.filtros_disponibles = json.loads(Variables.traer_variable("FILTROS_DISPONIBLES"))
