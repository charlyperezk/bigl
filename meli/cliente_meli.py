import requests
from requests import Response
from herramientas.excepciones import SolicitudError

class ClienteMeli:
    """
    ClienteMeli es el cliente encargado de realizar la solicitud a la API de Meli.
    Sin atributos
    """

    def solicitud_get(self, query: str, encabezados: dict) -> Response:
        """
        Realiza una solicitud GET a la API de Meli.

        Args:
            query (str): La URL de la solicitud.
            encabezados (dict): Los encabezados de la solicitud.

        Returns:
            Response: La respuesta de la solicitud.

        Raises:
            SolicitudError: Si ocurre un error en la solicitud.
        """
        try:
            return requests.get(
                url=query, headers=encabezados)
        except Exception as e:
            raise SolicitudError(f"Error en la solicitud GET. Mensaje : {str(e)}")

    def solicitud_post(self, url: str, datos: dict, encabezados: dict) -> Response:
        """
        Realiza una solicitud POST a la API de Meli.

        Args:
            datos (dict): Los datos para la solicitud POST.
            encabezados (dict): Los encabezados de la solicitud.

        Returns:
            Response: La respuesta de la solicitud.

        Raises:
            SolicitudError: Si ocurre un error en la solicitud.
        """
        try:
            return requests.post(
                url=url, data=datos, headers=encabezados)
        except Exception as e:
            raise SolicitudError(f"Error en la solicitud POST. Mensaje : {str(e)}")
