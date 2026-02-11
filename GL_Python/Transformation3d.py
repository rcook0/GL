
import math
from .Point3d import Point3d

class Transformation3d:
    """3D homogeneous transformation matrix."""

    def __init__(self):
        self.m = [[0.0]*4 for _ in range(4)]
        for i in range(4):
            self.m[i][i] = 1.0

    def transform(self, other: "Transformation3d") -> None:
        result = [[0.0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] += self.m[i][k] * other.m[k][j]
        self.m = result

    def translate(self, dx: float, dy: float, dz: float) -> None:
        t = Transformation3d()
        t.m[0][3] = dx
        t.m[1][3] = dy
        t.m[2][3] = dz
        self.transform(t)

    def scale(self, sx: float, sy: float, sz: float) -> None:
        s = Transformation3d()
        s.m[0][0] = sx
        s.m[1][1] = sy
        s.m[2][2] = sz
        self.transform(s)

    def rotate_x(self, theta: float) -> None:
        r = Transformation3d()
        c, s = math.cos(theta), math.sin(theta)
        r.m[1][1] = c;  r.m[1][2] = -s
        r.m[2][1] = s;  r.m[2][2] = c
        self.transform(r)

    def rotate_y(self, theta: float) -> None:
        r = Transformation3d()
        c, s = math.cos(theta), math.sin(theta)
        r.m[0][0] = c;  r.m[0][2] = s
        r.m[2][0] = -s; r.m[2][2] = c
        self.transform(r)

    def rotate_z(self, theta: float) -> None:
        r = Transformation3d()
        c, s = math.cos(theta), math.sin(theta)
        r.m[0][0] = c;  r.m[0][1] = -s
        r.m[1][0] = s;  r.m[1][1] = c
        self.transform(r)

    def shearZ(self, shx: float, shy: float) -> None:
        """
        Shear so that: x' = x + shx*z, y' = y + shy*z, z' = z
        """
        sh = Transformation3d()
        sh.m[0][2] = shx
        sh.m[1][2] = shy
        self.transform(sh)

    def viewingRotation(self, vpn, vup) -> None:
        """
        Rotate world coords so that:
          - n (from vpn) aligns with +z
          - u (from vup x n) aligns with +x
          - v (from n x u) aligns with +y
        Accepts vpn/vup as (x,y,z) tuples or objects with x(),y(),z()
        """
        def _vec3(a):
            if hasattr(a, "x"):
                return (a.x(), a.y(), a.z())
            if callable(getattr(a, "x", None)):
                return (a.x(), a.y(), a.z())
            return (a[0], a[1], a[2])

        def _norm(v):
            mag = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]) or 1.0
            return (v[0]/mag, v[1]/mag, v[2]/mag)

        def _cross(a, b):
            return (a[1]*b[2]-a[2]*b[1],
                    a[2]*b[0]-a[0]*b[2],
                    a[0]*b[1]-a[1]*b[0])

        n = _norm(_vec3(vpn))
        up = _norm(_vec3(vup))
        u = _norm(_cross(up, n))
        v = _cross(n, u)  # already orthogonal

        # Rotation that maps world -> VRC with axes rows [u; v; n]
        r = Transformation3d()
        r.m[0][0], r.m[0][1], r.m[0][2] = u
        r.m[1][0], r.m[1][1], r.m[1][2] = v
        r.m[2][0], r.m[2][1], r.m[2][2] = n
        self.transform(r)

    def apply_point(self, p: Point3d) -> Point3d:
        x, y, z = p.x(), p.y(), p.z()
        vec = [x, y, z, 1.0]
        res = [0.0]*4
        for i in range(4):
            for j in range(4):
                res[i] += self.m[i][j] * vec[j]
        if abs(res[3]) > 1e-9:
            return Point3d(res[0]/res[3], res[1]/res[3], res[2]/res[3])
        else:
            return Point3d(res[0], res[1], res[2])

    def __matmul__(self, p: Point3d) -> Point3d:
        return self.apply_point(p)

    def __str__(self):
        return "\n".join([" ".join(f"{v: .3f}" for v in row) for row in self.m])
