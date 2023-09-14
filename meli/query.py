from meli.filtro import Filtros
from meli.variables import Variables
from herramientas.excepciones import FiltroError, URLError
import logging

class Query:
    """
    Querys se encarga de la formulación de los endpoints.
    Sin atributos
    """

    def __init__(self, filtros: Filtros) -> None:
        """
        Inicializa una instancia de Query.

        Args:
            filtros (Filtros): Una instancia de la clase Filtros que contiene los filtros seleccionados por el usuario.
        """
        self._filtros = filtros

    def url_busqueda(self) -> str:
        """
        Obtiene la URL base para las búsquedas desde las variables de entorno.

        Returns:
            str: La URL base para las búsquedas.
        """
        return Variables.traer_variable("URL_BUSQUEDA")

    def url(self) -> str:
        """
        Genera la URL completa para la solicitud de búsqueda.

        Returns:
            str: La URL completa para la solicitud de búsqueda.

        Raises:
            FiltroError: Si no se encuentran filtros seleccionados.
            URLError: Si ocurre un error al generar la URL.
        """
        try:
            filtros_seleccionados = self._filtros.filtros_aplicados
            if len(self._filtros.filtros_aplicados) == 0:
                logging.error("No se han encontrado filtros para generar la query.")
                raise FiltroError("No se han encontrado filtros para generar la query.")
            url_base = self.url_busqueda()
            query = "&".join(filtros_seleccionados)
            url = f"{url_base}?{query}"
            return url
        except FiltroError as e:
            logging.error(f"Filtro error - Mensaje: {str(e)}")
        except Exception as e:
            logging.error(f"URL error - Mensaje: {str(e)}")
            raise URLError("Ha habido un error al generar la URL para la solicitud.")
