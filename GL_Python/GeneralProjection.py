# graphics_package/GeneralProjection.py
import math
from .Projection3d import Projection3d
from .Point3d import Point3d
from .Point2d import Point2d

class GeneralProjection(Projection3d):
    """
    General perspective projection with arbitrary camera.
    - eye: camera position (Point3d)
    - target: look-at point (Point3d)
    - up: approximate up vector (Point3d, treated as direction)
    - fov: field of view in degrees
    - aspect: aspect ratio (width/height)
    - near, far: clipping planes
    """

    def __init__(self, eye: Point3d, target: Point3d, up: Point3d,
                 fov: float = 60.0, aspect: float = 1.0,
                 near: float = 1.0, far: float = 1000.0):
        super().__init__(focal_length=None)
        self.eye = eye
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

        self._build_matrices()

    def _normalize(self, v):
        mag = math.sqrt(sum(c*c for c in v))
        return tuple(c/mag for c in v)

    def _cross(self, a, b):
        return (a[1]*b[2] - a[2]*b[1],
                a[2]*b[0] - a[0]*b[2],
                a[0]*b[1] - a[1]*b[0])

    def _dot(self, a, b):
        return sum(ai*bi for ai, bi in zip(a, b))

    def _build_matrices(self):
        # Camera basis
        eye = (self.eye.x(), self.eye.y(), self.eye.z())
        target = (self.target.x(), self.target.y(), self.target.z())
        up = (self.up.x(), self.up.y(), self.up.z())

        forward = self._normalize((target[0]-eye[0], target[1]-eye[1], target[2]-eye[2]))
        right = self._normalize(self._cross(forward, up))
        true_up = self._cross(right, forward)

        # View matrix (rotation + translation)
        self.view = [
            [ right[0],  right[1],  right[2], -self._dot(right, eye)],
            [ true_up[0], true_up[1], true_up[2], -self._dot(true_up, eye)],
            [-forward[0],-forward[1],-forward[2],  self._dot(forward, eye)],
            [0, 0, 0, 1]
        ]

        # Perspective projection matrix
        f = 1.0 / math.tan(math.radians(self.fov) / 2)
        nf = 1 / (self.near - self.far)
        self.proj = [
            [f/self.aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self.far+self.near)*nf, 2*self.far*self.near*nf],
            [0, 0, -1, 0]
        ]

    def _apply_matrix(self, m, v):
        res = [0.0]*4
        for i in range(4):
            for j in range(4):
                res[i] += m[i][j] * v[j]
        return res

    def project(self, p: Point3d) -> Point2d:
        # Homogeneous vector
        v = [p.x(), p.y(), p.z(), 1.0]

        # Apply view then projection
        v_eye = self._apply_matrix(self.view, v)
        v_clip = self._apply_matrix(self.proj, v_eye)

        # Perspective divide
        if abs(v_clip[3]) > 1e-9:
            x_ndc = v_clip[0] / v_clip[3]
            y_ndc = v_clip[1] / v_clip[3]
        else:
            x_ndc, y_ndc = v_clip[0], v_clip[1]

        # Return normalized device coords (-1..1 range)
        return Point2d(x_ndc, y_ndc)

    def __str__(self):
        return f"GeneralProjection(eye={self.eye}, target={self.target}, fov={self.fov}, aspect={self.aspect})"
