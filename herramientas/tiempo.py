from datetime import datetime


class HerramientasDatetime:

    def diferencia_umbral(t1: datetime, t2: datetime, umbral: int) -> bool:
        diferencia = t2 - t1
        diferencia = diferencia.total_seconds()
        umbral = umbral * 60 * 60
        if diferencia > umbral:
            return True            
        else:
            return False