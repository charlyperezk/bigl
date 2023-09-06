import logging
import json

from meli.cliente_meli import ClienteMeli


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

    def extraer(self, query:str, encabezados: dict) -> json:
        solicitud = self._cliente_meli.solicitud_get(query=query, encabezados=encabezados)
        if solicitud.status_code == 200:
            logging.info(" Código de respuesta 200 -- Solicitud exitosa")
        else:
            logging.error(" La solicitud HTTP ha fallado")
        return solicitud.json()