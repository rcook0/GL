# graphics_package/igraphic_object3d.py
from abc import ABC, abstractmethod

class IGraphicObject3d(ABC):
    @abstractmethod
    def transform(self, matrix):
        """Apply a 3D transformation (Translation, Rotation, Scaling, etc.)."""
        pass

    @abstractmethod
    def to_2d(self):
        """Project this 3D object into one or more 2D primitives (Line2d, etc.)."""
        pass
