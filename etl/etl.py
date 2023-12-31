import logging
from base.cliente import ClienteBaseDeDatos
from meli.cliente_meli import ClienteMeli
from meli.administrador import AdministradorCredenciales
from meli.query import Query
from meli.filtro import Filtros
from etl.extractor import Extractor
from etl.transformador import Transformador
from etl.cargador import Cargador
from herramientas.excepciones import SolicitudError, ProcesadoError

class ETL:
    """
    ETL administra tareas de limpieza, transformación y carga de solicitudes, así como estado de credenciales y
    guardado en la base de datos.

    Atributos
    ----------
    cliente_bd: ClienteBaseDeDatos
        Interacción con la base de datos.
    cliente: ClienteMeli
        Solicitud a la API de Meli.
    administrador: AdministradorCredenciales
        Obtención y renovación de credenciales.
    extractor: Extractor
        Extracción de las solicitudes a través de ClienteMeli.
    transformador: Transformador
        Procesamiento de la respuesta obtenida. Obtención de datos relevantes.
    cargador: Cargador
        Distribución de los datos obtenidos. Ej: Exportar a csv.
    """

    def __init__(self, cliente_bd: ClienteBaseDeDatos, filtro: Filtros) -> None:
        self._cliente_bd = cliente_bd
        self._cliente = ClienteMeli()
        self._administrador = AdministradorCredenciales(cliente=self._cliente_bd, cliente_meli=self._cliente)
        self._extractor = Extractor(cliente_meli=self._cliente)
        self._transformador = Transformador()
        self._cargador = Cargador()
        self._filtro = filtro
        self._query = Query(filtros=self._filtro)
    
    def consulta(self) -> list:
        """
        Realiza una consulta a la API de Meli, procesa los resultados y los exporta a un archivo CSV.

        Raises:
            SolicitudError: Error en la solicitud a la API.
            ProcesadoError: Error en el procesamiento de los datos.
        """
        try:
            logging.info("Supervisando el estado de las credenciales ...")
            self._administrador.supervisar()
            credencial = self._administrador.credencial()
            logging.info("Realizando extracción ...")
            query = self._query.url()
            solicitud = self._extractor.extraer(query=query, encabezados=credencial)
            transformacion = self._transformador.transformar(response=solicitud)
            self._cargador.exportar_csv(respuesta_transformada=transformacion)
            #return transformacion
        except SolicitudError as e:
            logging.error(f"Solicitud error - Mensaje: {str(e)}")
            return
        except ProcesadoError as e:
            logging.error(f"Procesado error - Mensaje: {str(e)}")
            return
        except Exception as e:
            logging.error(F"Error no controlado. Mensaje: {str(e)}")
            return
