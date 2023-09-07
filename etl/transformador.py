from herramientas.procesado import Procesador
from herramientas.excepciones import ProcesadoError

import logging
import json

class Transformador:
    """
    Transformador realiza filtrado de resultados y administra el procesamiento de los datos.
    
    Atributos
    ----------
    procesador: Procesador
        Procesamiento de la respuesta.
    """

    def __init__(self):
        self._procesador = Procesador()

    def transformar(self, response: json) -> list:
        """
        Transforma y procesa la respuesta JSON de la búsqueda en una lista de resultados procesados.

        Args:
            response (json): Respuesta JSON de la búsqueda.

        Returns:
            list: Lista de resultados procesados, donde cada elemento es un diccionario con datos de un inmueble.
        """
        logging.info(f"Examinando respuesta ...")
        resultados = response.get("results", "")
        resultados_obtenidos = len(resultados)
        if resultados_obtenidos == 0:
            logging.warning("La búsqueda no tiene coincidencias")
        else:
            logging.info(f"Se han obtenido {resultados_obtenidos} respuestas")
            logging.info("Obteniendo datos de interés ...")
            try:
                resultados_procesados = self._procesador._procesar_inmuebles(
                    resultados=resultados)
                logging.info("Los datos se han procesado exitosamente")
                return resultados_procesados
            except:
                raise ProcesadoError("Error al procesar los datos de la respuesta.")

    def obtener_keys(self, response: json) -> str:
        """
        Imprime las claves (keys) de un objeto JSON en la respuesta.

        Args:
            response (json): Respuesta JSON a examinar.
        """
        keys = response.keys()
        logging.info(
            "Se han encontrado las siguientes claves en la response:")
        for e, i in enumerate(keys):
            print(e, "--", i)
