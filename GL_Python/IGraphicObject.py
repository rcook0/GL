# graphics_package/IGraphicObject.py

from abc import ABC, abstractmethod

class IGraphicObject(ABC):
    """
    Abstract base class for all graphic objects.
    """

    @abstractmethod
    def draw(self, g=None) -> None:
        pass

    @abstractmethod
    def erase(self, g=None) -> None:
        pass

    @abstractmethod
    def transform(self, trans) -> None:
        pass
