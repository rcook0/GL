"""
shapes.py
Primitive shape generators for 3D rendering.
Each function returns a list of Polygon3D triangles.

Assumptions:
- Point3d(x, y, z) exists.
- Polygon3D(...) supports:
    * Polygon3D() then add_vertex(...)
    * Polygon3D([p1, p2, p3])
    * Polygon3D(p1, p2, p3)
"""

import numpy as np
from point3d import Point3d
from polygon3d import Polygon3D

# ----------------------
# Hardcoded primitives
# ----------------------

def make_cube(size: float = 1.0):
    """Cube centered at origin, side length = size."""
    s = size / 2.0
    v = [
        Point3d(-s, -s, -s), Point3d( s, -s, -s),
        Point3d( s,  s, -s), Point3d(-s,  s, -s),
        Point3d(-s, -s,  s), Point3d( s, -s,  s),
        Point3d( s,  s,  s), Point3d(-s,  s,  s),
    ]
    faces = [
        (0,1,2), (0,2,3),      # back
        (4,6,5), (4,7,6),      # front
        (0,4,5), (0,5,1),      # bottom
        (3,2,6), (3,6,7),      # top
        (1,5,6), (1,6,2),      # right
        (0,3,7), (0,7,4),      # left
    ]
    return [Polygon3D(v[a], v[b], v[c]) for (a, b, c) in faces]


def make_tetrahedron(size: float = 1.0):
    """Tetrahedron centered at origin."""
    s = size / 2.0
    v = [
        Point3d( s,  s,  s),
        Point3d(-s, -s,  s),
        Point3d(-s,  s, -s),
        Point3d( s, -s, -s),
    ]
    faces = [(0,1,2), (0,3,1), (0,2,3), (1,3,2)]
    return [Polygon3D(v[a], v[b], v[c]) for (a, b, c) in faces]


# ----------------------
# Parametric primitives
# ----------------------

def make_cone(radius: float = 1.0, height: float = 2.0, n: int = 32):
    """Cone with circular base at z = -height/2 and apex at z = +height/2."""
    polys = []
    apex = Point3d(0.0, 0.0,  height / 2.0)
    base_c = Point3d(0.0, 0.0, -height / 2.0)

    angles = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    ring = [Point3d(radius * np.cos(a), radius * np.sin(a), -height / 2.0) for a in angles]

    for i in range(n):
        p0 = ring[i]
        p1 = ring[(i + 1) % n]
        polys.append(Polygon3D(apex, p0, p1))          # side
        polys.append(Polygon3D(base_c, p1, p0))        # base (winding to face outward)
    return polys


def make_sphere(radius: float = 1.0, n_lat: int = 16, n_lon: int = 32):
    """Parametric sphere (lat/lon tessellation)."""
    polys = []

    def sp(theta, phi):
        return Point3d(
            radius * np.sin(theta) * np.cos(phi),
            radius * np.sin(theta) * np.sin(phi),
            radius * np.cos(theta)
        )

    for i in range(n_lat):
        t1, t2 = np.pi * i / n_lat, np.pi * (i + 1) / n_lat
        for j in range(n_lon):
            p1, p2 = 2.0 * np.pi * j / n_lon, 2.0 * np.pi * (j + 1) / n_lon
            a = sp(t1, p1); b = sp(t2, p1); c = sp(t2, p2); d = sp(t1, p2)
            if i != 0:
                polys.append(Polygon3D(a, b, c))
            if i != n_lat - 1:
                polys.append(Polygon3D(a, c, d))
    return polys


def make_torus(R: float = 1.0, r: float = 0.3, nu: int = 32, nv: int = 16):
    """Parametric torus (major radius R, minor radius r)."""
    polys = []

    def tp(u, v):
        return Point3d(
            (R + r * np.cos(v)) * np.cos(u),
            (R + r * np.cos(v)) * np.sin(u),
            r * np.sin(v)
        )

    for i in range(nu):
        u1, u2 = 2.0 * np.pi * i / nu, 2.0 * np.pi * (i + 1) / nu
        for j in range(nv):
            v1, v2 = 2.0 * np.pi * j / nv, 2.0 * np.pi * (j + 1) / nv
            p00, p01 = tp(u1, v1), tp(u1, v2)
            p10, p11 = tp(u2, v1), tp(u2, v2)
            polys.append(Polygon3D(p00, p10, p11))
            polys.append(Polygon3D(p00, p11, p01))
    return polys


# ----------------------
# Shape registry with sensible defaults
# ----------------------

def make_shapes_dict():
    """
    Registry mapping names → generator callables with defaults.
    Ideal for CLI dispatch; override params as needed at call sites.
    """
    return {
        "cube":        lambda: make_cube(size=1.0),
        "tetrahedron": lambda: make_tetrahedron(size=1.0),
        "cone":        lambda: make_cone(radius=1.0, height=2.0, n=32),
        "sphere":      lambda: make_sphere(radius=1.0, n_lat=16, n_lon=32),
        "torus":       lambda: make_torus(R=1.0, r=0.3, nu=32, nv=16),
    }
