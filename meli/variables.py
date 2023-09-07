import os
from dotenv import load_dotenv
from herramientas.excepciones import VariableError

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()

class Variables:
    """
    Variables accede a las variables de entorno.
    Sin atributos
    """

    @classmethod
    def traer_variable(cls, nombre_variable):
        """
        Obtiene el valor de una variable de entorno.

        Args:
            nombre_variable (str): El nombre de la variable de entorno que se desea obtener.

        Returns:
            str: El valor de la variable de entorno.

        Raises:
            VariableError: Si la variable de entorno no está definida en el archivo .env.
        """
        variable = os.getenv(nombre_variable)
        if variable is None:
            raise VariableError(f"No se ha podido acceder a la variable de entorno {nombre_variable}. Asegúrese de que está declarada en el archivo .env.")
        else:
            return variable
