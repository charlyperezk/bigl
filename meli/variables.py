import os

from dotenv import load_dotenv
load_dotenv()

class Variables:

    """
    Variables accede a las variables de entorno.
    Sin atributos

    """

    @classmethod
    def traer_variable(cls, nombre_variable):
        variable = os.getenv(nombre_variable)
        if variable is None:
            RuntimeError(" No se ha podido acceder a la variable de entorno {nombre_variable}. ")
        return variable