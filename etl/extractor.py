import logging
import json

from meli.cliente_meli import ClienteMeli
from herramientas.excepciones import SolicitudError

class Extractor:
    """
    Extractor administra la extracción de datos y manejo de errores en solicitudes.
    
    Atributos
    ----------
    cliente: ClienteMeli
        Solicitud a la API de Meli.
    """

    def __init__(self, cliente_meli: ClienteMeli) -> None:
        self._cliente_meli = cliente_meli

    def extraer(self, query: str, encabezados: dict) -> json:
        """
        Realiza una solicitud GET a la API de Meli y maneja los errores de respuesta.

        Args:
            query (str): URL de la solicitud GET.
            encabezados (dict): Encabezados de la solicitud.

        Returns:
            json: Respuesta JSON de la solicitud.

        Raises:
            SolicitudError: Error en la solicitud con el código de respuesta correspondiente.
        """
        solicitud = self._cliente_meli.solicitud_get(
            query=query, encabezados=encabezados)
        if solicitud.status_code == 200:
            logging.info(" Código de respuesta 200 -- Solicitud exitosa")
        else:
            logging.error(f"Solicitud error - Codigo de respuesta: {solicitud.status_code}")
            raise SolicitudError(f"La solicitud ha arrojado código de respuesta {solicitud.status_code}")
        return solicitud.json()
