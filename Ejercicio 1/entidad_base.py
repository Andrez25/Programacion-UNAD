from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    _contador_ids = 0

    def __init__(self, nombre):
        EntidadBase._contador_ids += 1
        self._id = EntidadBase._contador_ids
        self._nombre = nombre
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar(self):
        pass

    def __str__(self):
        return self.describir()

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id}, nombre={self._nombre!r})"
