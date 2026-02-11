# graphics_package/AxisAlignedProjection.py
import math
from .Projection3d import Projection3d
from .Point3d import Point3d
from .Point2d import Point2d

class AxisAlignedProjection(Projection3d):
    """
    Axis-aligned perspective projection.
    - 1-point: z-axis vanishes, x and y stay parallel.
    - 2-point: x and z vanish, y stays parallel (verticals preserved).
    - 3-point: x, y, z all vanish (full perspective).
    """

    MODE_1POINT = 1
    MODE_2POINT = 2
    MODE_3POINT = 3

    def __init__(self, mode: int = 2, focal_length: float = 500.0):
        super().__init__(focal_length)
        if mode not in (self.MODE_1POINT, self.MODE_2POINT, self.MODE_3POINT):
            raise ValueError("Projection mode must be 1, 2, or 3")
        self.mode = mode

    def project(self, p: Point3d) -> Point2d:
        x, y, z = p.x(), p.y(), p.z()
        f = self.focal_length

        # Default: orthographic projection (no scaling)
        X, Y = x, y

        if self.mode == self.MODE_1POINT:
            # Only z vanishes
            if (f + z) != 0:
                X = x * f / (f + z)
                Y = y * f / (f + z)

        elif self.mode == self.MODE_2POINT:
            # x and z vanish, y stays parallel
            if (f + z) != 0:
                X = x * f / (f + z)
            if (f + x) != 0:
                Y = y * f / (f + x)

        elif self.mode == self.MODE_3POINT:
            # x, y, z all vanish
            if (f + z) != 0:
                X = x * f / (f + z)
            if (f + x) != 0:
                Y = y * f / (f + x)
            # extra vanishing on y vs z
            if (f + y) != 0:
                Y = Y * f / (f + y)

        return Point2d(X, Y)

    def __str__(self):
        return f"AxisAlignedProjection(mode={self.mode}, f={self.focal_length})"
