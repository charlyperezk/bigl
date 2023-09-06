from herramientas.procesado import Procesador

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
        logging.info(f" Examinando respuesta ... ")
        resultados = response.get("results", "")
        resultados_obtenidos = len(resultados)
        logging.info(f" Se han obtenido {resultados_obtenidos} respuestas ")
        logging.info(" Obteniendo datos de interés ... ")
        items_procesados = self._procesador._procesar_inmuebles(resultados=resultados)
        logging.info(" Los datos se han procesado exitosamente ")
        return items_procesados

    def obtener_keys(self, response: json) -> str:
        keys = response.keys()
        logging.info(" Se han encontrado las siguientes claves en la response: ")
        for e, i in enumerate(keys):
            print (e, "--", i)