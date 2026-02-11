# graphics_package/polygon3d.py
from graphics_package.point3d import Point3d
from graphics_package.igraphic_object3d import IGraphicObject3d


class Polygon3d(IGraphicObject3d):
    def __init__(self, vertices=None):
        self.vertices = vertices if vertices is not None else []

    def add_vertex(self, p: Point3d):
        self.vertices.append(p)

    def transform(self, matrix):
        for v in self.vertices:
            v.transform(matrix)

    def to_2d(self):
        from graphics_package.line2d import Line2d
        lines = []
        if len(self.vertices) < 2:
            return lines
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            lines.append(Line2d(p1.x(), p1.y(), p2.x(), p2.y()))
        return lines

    # ------------------------------
    # Main tessellation dispatcher
    # ------------------------------

    def triangulate(self, subdiv=1):
        """
        Return a list of Polygon3d triangles approximating this polygon.
        - 3: subdivided barycentrically
        - 4: subdivided bilinearly
        - 6: subdivided radially (hex grid)
        - 8: subdivided radially (octagon wedges)
        - primes up to 23: subdivided fan wedges
        - else: fan triangulation
        """
        n = len(self.vertices)
        if n < 3:
            return []

        if n == 3:
            return self._subdivide_triangle(subdiv)
        elif n == 4:
            return self._subdivide_quad(subdiv)
        elif n == 6:
            return self._subdivide_hexagon(subdiv)
        elif n == 8:
            return self._subdivide_octagon(subdiv)
        elif n in {5, 7, 11, 13, 17, 19, 23}:
            return self._subdivide_prime_ngon(subdiv)
        else:
            return self._fan_triangulate()

    # ------------------------------
    # Helpers
    # ------------------------------

    def _fan_triangulate(self):
        tris = []
        v0 = self.vertices[0]
        for i in range(1, len(self.vertices) - 1):
            tris.append(Polygon3d([v0, self.vertices[i], self.vertices[i + 1]]))
        return tris

    def _subdivide_triangle(self, subdiv):
        """Subdivide a triangle into smaller ones using barycentric interpolation."""
        v0, v1, v2 = self.vertices
        tris = []

        # Generate barycentric grid
        grid = {}
        for i in range(subdiv + 1):
            for j in range(subdiv + 1 - i):
                a = i / subdiv
                b = j / subdiv
                c = 1 - a - b
                x = a * v0.x() + b * v1.x() + c * v2.x()
                y = a * v0.y() + b * v1.y() + c * v2.y()
                z = a * v0.z() + b * v1.z() + c * v2.z()
                grid[(i, j)] = Point3d(x, y, z)

        # Build triangles from grid
        for i in range(subdiv):
            for j in range(subdiv - i):
                p1 = grid[(i, j)]
                p2 = grid[(i + 1, j)]
                p3 = grid[(i, j + 1)]
                tris.append(Polygon3d([p1, p2, p3]))
                if j + 1 <= subdiv - i - 1:
                    p4 = grid[(i + 1, j + 1)]
                    tris.append(Polygon3d([p2, p4, p3]))
        return tris

    def _subdivide_quad(self, subdiv):
        """Subdivide a quad into a grid, then split each sub-quad into two triangles."""
        v0, v1, v2, v3 = self.vertices  # convex quad

        def bilerp(s, t):
            return Point3d(
                (1 - s) * (1 - t) * v0.x() + s * (1 - t) * v1.x() + s * t * v2.x() + (1 - s) * t * v3.x(),
                (1 - s) * (1 - t) * v0.y() + s * (1 - t) * v1.y() + s * t * v2.y() + (1 - s) * t * v3.y(),
                (1 - s) * (1 - t) * v0.z() + s * (1 - t) * v1.z() + s * t * v2.z() + (1 - s) * t * v3.z(),
            )

        grid = [[None] * (subdiv + 1) for _ in range(subdiv + 1)]
        for i in range(subdiv + 1):
            for j in range(subdiv + 1):
                grid[i][j] = bilerp(i / subdiv, j / subdiv)

        tris = []
        for i in range(subdiv):
            for j in range(subdiv):
                p00 = grid[i][j]
                p10 = grid[i + 1][j]
                p11 = grid[i + 1][j + 1]
                p01 = grid[i][j + 1]
                tris.append(Polygon3d([p00, p10, p11]))
                tris.append(Polygon3d([p00, p11, p01]))
        return tris

    def _subdivide_hexagon(self, subdiv):
        """Subdivide hexagon into radial wedges, then refine each wedge."""
        cx = sum(v.x() for v in self.vertices) / 6
        cy = sum(v.y() for v in self.vertices) / 6
        cz = sum(v.z() for v in self.vertices) / 6
        center = Point3d(cx, cy, cz)

        tris = []
        for i in range(6):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % 6]
            wedge = Polygon3d([center, v1, v2])
            tris.extend(wedge._subdivide_triangle(subdiv))
        return tris

    def _subdivide_octagon(self, subdiv):
        """Subdivide octagon into 8 radial wedges, then refine each wedge."""
        cx = sum(v.x() for v in self.vertices) / 8
        cy = sum(v.y() for v in self.vertices) / 8
        cz = sum(v.z() for v in self.vertices) / 8
        center = Point3d(cx, cy, cz)

        tris = []
        for i in range(8):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % 8]
            wedge = Polygon3d([center, v1, v2])
            tris.extend(wedge._subdivide_triangle(subdiv))
        return tris

    def _subdivide_prime_ngon(self, subdiv):
        """Subdivide prime-sided polygon into N fan wedges, each refined."""
        n = len(self.vertices)
        cx = sum(v.x() for v in self.vertices) / n
        cy = sum(v.y() for v in self.vertices) / n
        cz = sum(v.z() for v in self.vertices) / n
        center = Point3d(cx, cy, cz)

        tris = []
        for i in range(n):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % n]
            wedge = Polygon3d([center, v1, v2])
            tris.extend(wedge._subdivide_triangle(subdiv))
        return tris

    # ------------------------------
    # Utility
    # ------------------------------

    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices)

    def __str__(self):
        verts_str = ", ".join(str(v) for v in self.vertices)
        return f"Polygon3d({verts_str})"
