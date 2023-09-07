from meli.variables import Variables

import json


class Filtros:

    """
    Filtros se encarga del manejo de filtros de búsqueda. Almacena la selección de filtros del usuario.
    Pueden agregarse filtros a través del archivo .env
    Sin atributos

    """
    
    filtros_aplicados = []

    @classmethod
    def _filtros(cls, mostrar: bool=False) -> json:
        filtros = json.loads(Variables.traer_variable("FILTROS_DISPONIBLES"))
        if mostrar:
            print(f" Filtros de búsqueda disponibles: ")
            print("")
            for e, filtro_dispobible in enumerate(filtros):
                print(e+1, "--", filtro_dispobible.lower())
            print("")
            return filtros
        return filtros

    @classmethod
    def _opciones(cls, nombre_filtro: str, mostrar: bool=False, llaves: bool=False) -> list or dict:
        disponibles = cls._filtros()
        if nombre_filtro not in disponibles:
            RuntimeError(" El filtro seleccionado no se encuentra dentro de los disponibles ")
        filtro = Variables.traer_variable(nombre_variable=nombre_filtro)
        filtro = json.loads(filtro)
        opciones = list(filtro.keys())
        if mostrar:
            print(f" Opciones de {nombre_filtro.lower()} son: ")
            print("")
            for e, opcion in enumerate(opciones[1:]):
                print(e+1, "--", opcion)
            print("")
        if llaves:
            return opciones[1:]
        else:
            return filtro
    
    @classmethod
    def _seleccionar_filtro(cls, filtro_seleccionado: tuple) -> None:
        disponibles = cls._filtros()
        nombre_filtro = filtro_seleccionado[0]
        opcion = filtro_seleccionado[1]
        if nombre_filtro not in disponibles:
            RuntimeError(" El filtro seleccionado no se encuentra dentro de los disponibles ")
        opciones_filtro = cls._opciones(nombre_filtro=nombre_filtro)
        llaves_opciones = list(cls._opciones(nombre_filtro=nombre_filtro, llaves=True))
        opcion_seleccionada = llaves_opciones[opcion]
        query = opciones_filtro["ID"].lower()+opciones_filtro[opcion_seleccionada]
        cls.filtros_aplicados.append(query)
        print("")
        print(" Se ha añadido el filtro exitosamente ")

    @classmethod
    def _seleccion(cls, mostrar: bool=False) -> list:
        seleccion = cls.filtros_aplicados
        if mostrar:
            print("")
            print(" Filtros aplicados: ")
            for filtro in seleccion:
                print("")
                print(f" - {filtro}")
            print("")
        return seleccion