import requests
from requests import Response


class ClienteMeli:

    """
    ClienteMeli es el cliente encargado de realizar la solicitud a la API de Meli.
    Sin atributos

    """
    
    def solicitud_get(self, query: str, encabezados: dict) -> Response:
        return requests.get(
            url=query, headers=encabezados)