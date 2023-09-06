from sqlalchemy import func
from sqlalchemy.orm import Session


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
        self._session.add(object)
        self._session.commit()

    def ultimo_registro(self, object):
        data = self._session.query(object).order_by(object.id.desc()).first()
        self.session_commit()
        return data
    
    def registros(self, object):
        data = self._session.query(object).all()
        return data

    def session_commit(self) -> None:
        self._session.commit()