from datetime import datetime

class HerramientasDatetime:

    def es_superado_umbral(t1: datetime, t2: datetime, umbral: int) -> bool:
        """
        Comprueba si la diferencia entre dos marcas de tiempo (datetime) supera un umbral dado en horas.

        Args:
            t1 (datetime): La primera marca de tiempo.
            t2 (datetime): La segunda marca de tiempo.
            umbral (int): El umbral en horas a verificar.

        Returns:
            bool: True si la diferencia supera el umbral, False de lo contrario.
        """
        diferencia = t2 - t1
        diferencia = diferencia.total_seconds()
        umbral = umbral * 60 * 60
        return diferencia > umbral

