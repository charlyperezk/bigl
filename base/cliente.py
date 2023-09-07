from sqlalchemy import func
from sqlalchemy.orm import Session

from herramientas.excepciones import BaseDeDatosError


class ClienteBaseDeDatos:
    """
    Cliente para interacción con la base de datos.
    Atributos
    ----------
    session: Session
       SQLAlchemy session.
    """

    def __init__(self, sesion: Session) -> None:
        self._session = sesion

    def guardar(self, object) -> None:
        try:
            self._session.add(object)
            self._session.commit()
        except:
            raise BaseDeDatosError("Error al guardar.")

    def ultimo_registro(self, object):
        try:
            data = self._session.query(object).order_by(object.id.desc()).first()
            self.session_commit()
            return data
        except:
            raise BaseDeDatosError("Error al consultar el último registro.")

    def registros(self, object):
        try:
            data = self._session.query(object).all()
            return data
        except:
            raise BaseDeDatosError("Error al solicitar los registros.")

    def session_commit(self) -> None:
        self._session.commit()