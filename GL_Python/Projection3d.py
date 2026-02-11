# graphics_package/Projection3d.py
from abc import ABC, abstractmethod
from .Point3d import Point3d
from .Point2d import Point2d

class Projection3d(ABC):
    """
    Abstract base for 3D → 2D projections.
    Subclasses implement specific strategies (axis-aligned, general camera, etc.).
    """

    def __init__(self, focal_length: float = 500.0):
        # Focal length or projection distance, in arbitrary units.
        self.focal_length = focal_length

    @abstractmethod
    def project(self, p: Point3d) -> Point2d:
        """
        Project a 3D point into 2D screen coordinates.
        Must be implemented by subclasses.
        """
        pass

    def project_line(self, line3d: "Line3d") -> "Line2d":
        """
        Project a 3D line by projecting its endpoints.
        """
        src2d = self.project(line3d.getSourcePoint())
        dst2d = self.project(line3d.getDestinationPoint())
        from .Line2d import Line2d
        return Line2d(src2d.x(), src2d.y(), dst2d.x(), dst2d.y())

    def __call__(self, p: Point3d) -> Point2d:
        """
        Shorthand: proj(point) instead of proj.project(point).
        """
        return self.project(p)
