# Clase plantilla para el resto de clases (menus)

from abc import ABC, abstractmethod

class State(ABC):
    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abstractmethod
    def ejecutar(self):
        """Cada estado debe implementar su propia lógica de ejecución."""
        pass
