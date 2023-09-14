import logging
from base.cliente import ClienteBaseDeDatos
from base.modelos.conexion import Conexion
from meli.credenciales import Credenciales
from meli.cliente_meli import ClienteMeli
from herramientas.excepciones import CredencialesError, SolicitudError, BaseDeDatosError

class AdministradorCredenciales:
    """
    AdministradorCredenciales se encarga de la autenticación. Administra la obtención, renovación y supervisión
    del estado actual de las credenciales, necesarias si se quiere interactuar con la API.

    Atributos
    ----------
    cliente_bd: ClienteBaseDeDatos
        Interacción con la base de datos.
    credenciales: Credenciales
        Credenciales del usuario.
    credenciales_url: str
        URL para operar credenciales.
    """

    def __init__(self, cliente: ClienteBaseDeDatos, cliente_meli: ClienteMeli) -> None:
        self._cliente = cliente
        self._cliente_meli = cliente_meli
        self._credenciales = Credenciales
        self.credenciales_url = "https://api.mercadolibre.com/oauth/token"

    def credencial(self) -> dict:
        """
        Obtiene las credenciales de acceso.

        Returns:
            dict: Encabezados con las credenciales.
        """
        conexion = self._cliente.ultimo_registro(object=Conexion)
        access_token = conexion.access_token
        if access_token is None:
            logging.error("No se localizó el access token")
            raise CredencialesError("No se encontró registro del último access token.")
        encabezados = {
            'Authorization': f"Bearer {access_token}"
        }
        return encabezados

    def supervisar(self) -> None:
        """
        Supervisa y gestiona las credenciales de forma automática.
        """
        try:
            registros = self._cliente.registros(object=Conexion)
            if len(registros) == 0:
                logging.info("No se han encontrado registros de credenciales almacenados")
                datos, encabezados = self._credenciales.credenciales_conexion(reconexion=False)
                logging.info("Solicitando credenciales ...")
                solicitud = self._cliente_meli.solicitud_post(url=self.credenciales_url, datos=datos, encabezados=encabezados)
                if solicitud.status_code == 200:
                    logging.info("Se han obtenido las nuevas credenciales satisfactoriamente.")
                    access_token = solicitud.json().get("access_token", "")
                    refresh_token = solicitud.json().get("refresh_token", "")
                    conexion = Conexion(refresh_token=refresh_token, access_token=access_token)
                    self._cliente.guardar(object=conexion)
                else:
                    logging.error(f"No se han podido obtener las credenciales. La solicitud ha devuelto codigo {solicitud.status_code}")
                    raise SolicitudError(f"No se obtuvieron las credenciales. Codigo de error de la request {solicitud.status_code}")
            else:
                ultimo_registro = self._cliente.ultimo_registro(Conexion)
                requiere_reconexion = self._credenciales.control_umbral(conexion=ultimo_registro)
                if requiere_reconexion == True:
                    refresh_token = ultimo_registro.refresh_token
                    logging.info("El último registro localizado requiere reconexion")
                    datos, encabezados = self._credenciales.credenciales_conexion(reconexion=True)
                    datos["refresh_token"] = refresh_token
                    logging.info("Reconectando ...")
                    solicitud = self._cliente_meli.solicitud_post(url=self.credenciales_url, datos=datos, encabezados=encabezados)
                    if solicitud.status_code == 200:
                        logging.info("Se han renovado las credenciales satisfactoriamente")
                        access_token = solicitud.json().get("access_token", "")
                        refresh_token = solicitud.json().get("refresh_token", "")
                        conexion = Conexion(refresh_token=refresh_token, access_token=access_token)
                        self._cliente.guardar(object=conexion)
                    else:
                        logging.error(f"No se han podido renovar las credenciales. La solicitud ha devuelto codigo {solicitud.status_code}")
                        raise SolicitudError(f"No se renovaron las credenciales. Codigo de error de la request {solicitud.status_code}")
                else:
                    logging.info(f"Las credenciales son válidas. La última fecha de conexión es {ultimo_registro.fecha_conexion}")
        except SolicitudError as e:
            logging.error(f"Solicitud error - Mensaje: {str(e)}")
        except BaseDeDatosError as e:
            logging.error(f"Base de datos error - Mensaje: {str(e)}")
