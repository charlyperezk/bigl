import os

from dotenv import load_dotenv
load_dotenv()

class Querys:

    """
    Querys se encarga de la formulación de los endpoints.
    Sin atributos

    """
    
    @classmethod
    def url_busqueda(cls) -> str:
        return os.getenv("URL_BUSQUEDA")
    
    @classmethod
    def filtro_coordenadas(cls, lat1: str, lat2: str, long1: str, long2: str) -> str:
        filtro = os.getenv("FILTRO_COORDENADAS")
        query = f"lat:{lat1}_{lat2},lon:{long1}_{long2}"
        return filtro + query

    @classmethod
    def filtro_categoria(cls, id_categoria: str) -> str:
        filtro = os.getenv("FILTRO_CATEGORIA")
        query = id_categoria
        return filtro + query

    @classmethod
    def url_consulta_geolocalizacion(cls, lat1: str, lat2: str, long1: str, long2: str) -> str:
        url_base = cls.url_busqueda()
        filtro_coord = cls.filtro_coordenadas(lat1, lat2, long1, long2)
        filtro_categoria = cls.filtro_categoria("MLA1459")
        url = f"{url_base}{filtro_coord}&{filtro_categoria}"
        return url