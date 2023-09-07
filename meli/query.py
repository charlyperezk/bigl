from meli.variables import Variables
from meli.filtro import Filtros

class Query:

    """
    Querys se encarga de la formulación de los endpoints.
    Sin atributos

    """

    def __init__(self, filtros: Filtros) -> None:
        self._filtros = filtros

    def url_busqueda(self) -> str:
        return Variables.traer_variable("URL_BUSQUEDA")

    def url(self) -> str:
        filtros_seleccionados = self._filtros.filtros_aplicados
        if len(self._filtros.filtros_aplicados) == 0:
            RuntimeError(" No hay filtros aplicados ")
        url_base = self.url_busqueda()
        query = "&".join(filtros_seleccionados)
        url = f"{url_base}?{query}"
        return url