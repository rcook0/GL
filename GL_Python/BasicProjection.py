# graphics_package/BasicProjection.py
from .Matrix import Matrix
from .Point3d import Point3d

"""
def perspective(d: float) -> Matrix:
    # p' = M * p, w' = z/d -> divide to get (d*x/z, d*y/z)
    return Matrix.from_list([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,1/d,0],
    ])

def orthographic() -> Matrix:
    # drop z, keep x,y
    return Matrix.from_list([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,0,0],
        [0,0,0,1],
    ])
"""

class BasicProjection(Matrix):
    """
    Python port of BasicProjection.
    Implements perspective and orthographic projections.
    """

    def __init__(self):
        super().__init__(4, 4, 0.0)
        self.m[0][0] = 1.0
        self.m[1][1] = 1.0

    def perspective(self, d: float) -> None:
        """
        Perspective projection (center of projection at origin, plane z=d).
        """
        self.m[2][2] = 1.0
        self.m[3][2] = 1.0 / d

    def perspectiveII(self, d: float) -> None:
        """
        Alternative perspective projection.
        """
        self.m[3][2] = 1.0 / d
        self.m[3][3] = 1.0

    def orthographic(self) -> None:
        """
        Orthographic projection (direction parallel to z-axis).
        """
        self.m[3][3] = 0.0

    def general(self, Q: float, p: Point3d, d: list[float]) -> None:
        """
        Generalized projection matrix (unifies perspective/orthographic).
        d is a normalized direction vector [dx, dy, dz].
        """
        dx, dy, dz = d
        self.m[0][2] = -(dx / dz)
        self.m[0][3] = p.z() * (dx / dz)
        self.m[1][2] = -(dy / dz)
        self.m[1][3] = p.z() * (dy / dz)
        self.m[2][2] = -(p.z() / (Q * dz))
        self.m[2][3] = (p.x() ** 2) / (Q * dz) + p.z()
        self.m[3][2] = -1.0 / (Q * dz)
        self.m[3][3] = 1.0 + (p.z() / (Q * dz))
