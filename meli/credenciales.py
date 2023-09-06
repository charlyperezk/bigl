import os

from datetime import datetime

from herramientas.tiempo import HerramientasDatetime as tiempo

from dotenv import load_dotenv
load_dotenv()


class Credenciales:

    """
    Credenciales administra los datos proveídos por el usuario. 
    Sin atributos

    """

    @classmethod
    def credenciales_conexion(self, reconexion: bool) -> dict:
        id_cliente = os.getenv("CLIENT_ID")
        cliente_secreto = os.getenv("CLIENT_SECRET")
        url_redireccion = os.getenv("REDIRECT_URI")
        code = os.getenv("CODE")
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