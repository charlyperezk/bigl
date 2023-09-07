from datetime import datetime
from meli.variables import Variables
from herramientas.tiempo import HerramientasDatetime as tiempo
from herramientas.excepciones import VariableError, CredencialesError
import logging

class Credenciales:
    """
    Credenciales administra los datos proporcionados por el usuario.
    Sin atributos
    """

    @classmethod
    def credenciales_conexion(cls, reconexion: bool) -> dict:
        """
        Obtiene las credenciales de conexión necesarias para interactuar con la API de Mercado Libre.

        Args:
            reconexion (bool): Indica si se trata de una reconexión.

        Returns:
            dict: Los datos de autenticación y los encabezados para realizar la solicitud.

        Raises:
            CredencialesError: Si ocurre un error al obtener las credenciales de conexión.
        """
        try:
            id_cliente = Variables.traer_variable("CLIENT_ID")
            cliente_secreto = Variables.traer_variable("CLIENT_SECRET")
            url_redireccion = Variables.traer_variable("REDIRECT_URI")
            code = Variables.traer_variable("CODE")
            encabezados = {
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded"
            }
            if not reconexion:
                datos = {
                    "grant_type": "authorization_code",
                    "client_id": f"{id_cliente}",
                    "client_secret": f"{cliente_secreto}",
                    "code": f"{code}",
                    "redirect_uri": f"{url_redireccion}"
                }
                return datos, encabezados
            else:
                datos = {
                    "grant_type": "refresh_token",
                    "client_id": f"{id_cliente}",
                    "client_secret": f"{cliente_secreto}",
                    "redirect_uri": f"{url_redireccion}"
                }
                return datos, encabezados
        except VariableError:
            logging.error("No se encontraron las variables de entorno.")
            raise CredencialesError("Error al obtener las credenciales de conexión. Recuerde que para interactuar con la API de Mercado Libre, debe ingresar su CLIENT_ID, CLIENT_SECRET, REDIRECT_URI y CODE.")

    @classmethod
    def control_umbral(cls, conexion) -> bool:
        """
        Controla si se debe reconectar a la API basándose en el umbral de tiempo.

        Args:
            conexion: El objeto de conexión con información sobre la última conexión.

        Returns:
            bool: True si se debe reconectar, False en caso contrario.
        """
        t1 = conexion.fecha_conexion
        ahora = datetime.now()
        reconectar = tiempo.es_superado_umbral(t1, t2=ahora, umbral=4)
        return reconectar
