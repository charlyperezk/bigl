import pandas as pd

import logging


class Cargador:

    """
    Cargador administra el destino final de la solicitud que ha realizado el usuario, ya procesada.
    Sin atributos

    """

    def exportar_csv(self, respuesta_transformada: dict) -> None:
        nombre = "datos.csv"
        directorio = f"exportados/{nombre}"
        df = pd.DataFrame(respuesta_transformada)
        df.to_csv(directorio, index=False)
        logging.info(f" Archivo exportado en la dirección {directorio} con el nombre {nombre} ")

