from abc import ABC, abstractmethod
from .IGraphicObject import IGraphicObject

class ICompoundGraphicObject2d(IGraphicObject, ABC):
    """
    Abstract interface for compound 2D graphic objects.
    Extends IGraphicObject.
    """

    @abstractmethod
    def add(self, obj: IGraphicObject) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
