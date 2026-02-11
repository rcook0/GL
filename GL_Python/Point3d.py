import numpy as np

class Point3d:
    def __init__(self, x, y, z, nx=0.0, ny=0.0, nz=1.0):
        self._x = x
        self._y = y
        self._z = z
        self.nx = nx
        self.ny = ny
        self.nz = nz

    def x(self): return self._x
    def y(self): return self._y
    def z(self): return self._z

    def set(self, x, y, z):
        self._x, self._y, self._z = x, y, z

    def normalize_normal(self):
        n = np.array([self.nx, self.ny, self.nz], dtype=np.float32)
        norm = np.linalg.norm(n)
        if norm > 1e-8:
            n /= norm
        self.nx, self.ny, self.nz = n.tolist()

    def __repr__(self):
        return f"Point3d({self._x:.2f}, {self._y:.2f}, {self._z:.2f}, n=({self.nx:.2f},{self.ny:.2f},{self.nz:.2f}))"
