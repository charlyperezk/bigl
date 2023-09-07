from base.cliente import ClienteBaseDeDatos
from meli.cliente_meli import ClienteMeli
from meli.administrador import AdministradorCredenciales
from meli.query import Query
from meli.filtro import Filtros
from etl.extractor import Extractor
from etl.transformador import Transformador
from etl.cargador import Cargador

import logging


class ETL:

    """
    ETL administra tareas de limpieza, transformación y carga de solicitudes, asícomo estado de credenciales y guardado en la base de datos.
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
        self._administrador = AdministradorCredenciales(cliente=self._cliente_bd)
        self._extractor = Extractor(cliente_meli=self._cliente)
        self._transformador = Transformador()
        self._cargador = Cargador()
        self._filtro = filtro
        self._query = Query(filtros=self._filtro)
    
    def consulta(self, mostrar: bool=False) -> list:
        logging.info(" Supervisando el estado de las credenciales ... ")
        self._administrador.supervisar()
        credencial = self._administrador.credencial()
        logging.info(" Realizando extracción ")
        query = self._query.url()
        solicitud = self._extractor.extraer(
            query=query, encabezados=credencial)
        transformacion = self._transformador.transformar(response=solicitud)
        self._cargador.exportar_csv(respuesta_transformada=transformacion)
        return transformacion