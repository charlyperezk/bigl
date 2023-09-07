from datetime import datetime

from meli.variables import Variables
from herramientas.tiempo import HerramientasDatetime as tiempo



class Credenciales:

    """
    Credenciales administra los datos proveídos por el usuario. 
    Sin atributos

    """

    @classmethod
    def credenciales_conexion(self, reconexion: bool) -> dict:
        id_cliente = Variables.traer_variable("CLIENT_ID")
        cliente_secreto = Variables.traer_variable("CLIENT_SECRET")
        url_redireccion = Variables.traer_variable("REDIRECT_URI")
        code = Variables.traer_variable("CODE")
        encabezados = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }
        if reconexion is False:
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

    @classmethod
    def control_umbral(self, object) -> bool:
        t1 = object.fecha_conexion
        ahora = datetime.now()
        reconectar = tiempo.diferencia_umbral(t1, t2=ahora, umbral=4)
        return reconectar