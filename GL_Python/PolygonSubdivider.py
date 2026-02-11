from graphics_package.point3d import Point3d

class PolygonSubdivider:

    # --------------------------
    # TRIANGLE
    # --------------------------
    def _subdivide_triangle(self, v0, v1, v2, subdivisions=1):
        """Subdivide a triangle into smaller triangles with normal interpolation."""
        grid = {}
        for i in range(subdivisions + 1):
            for j in range(subdivisions - i + 1):
                a = i / subdivisions
                b = j / subdivisions
                c = 1 - a - b
                x = a * v0.x() + b * v1.x() + c * v2.x()
                y = a * v0.y() + b * v1.y() + c * v2.y()
                z = a * v0.z() + b * v1.z() + c * v2.z()

                nx = a * v0.nx + b * v1.nx + c * v2.nx
                ny = a * v0.ny + b * v1.ny + c * v2.ny
                nz = a * v0.nz + b * v1.nz + c * v2.nz

                p = Point3d(x, y, z, nx, ny, nz)
                p.normalize_normal()
                grid[(i, j)] = p

        triangles = []
        for i in range(subdivisions):
            for j in range(subdivisions - i):
                p0 = grid[(i, j)]
                p1 = grid[(i + 1, j)]
                p2 = grid[(i, j + 1)]
                triangles.append((p0, p1, p2))
                if j + i < subdivisions - 1:
                    p3 = grid[(i + 1, j + 1)]
                    triangles.append((p1, p3, p2))
        return triangles

    # --------------------------
    # QUAD
    # --------------------------
    def _subdivide_quad(self, v0, v1, v2, v3, subdivisions=1):
        """Subdivide a quad into smaller triangles with normal interpolation."""
        grid = {}
        for i in range(subdivisions + 1):
            for j in range(subdivisions + 1):
                a = i / subdivisions
                b = j / subdivisions

                x = (1 - a) * ((1 - b) * v0.x() + b * v1.x()) + a * ((1 - b) * v3.x() + b * v2.x())
                y = (1 - a) * ((1 - b) * v0.y() + b * v1.y()) + a * ((1 - b) * v3.y() + b * v2.y())
                z = (1 - a) * ((1 - b) * v0.z() + b * v1.z()) + a * ((1 - b) * v3.z() + b * v2.z())

                nx = (1 - a) * ((1 - b) * v0.nx + b * v1.nx) + a * ((1 - b) * v3.nx + b * v2.nx)
                ny = (1 - a) * ((1 - b) * v0.ny + b * v1.ny) + a * ((1 - b) * v3.ny + b * v2.ny)
                nz = (1 - a) * ((1 - b) * v0.nz + b * v1.nz) + a * ((1 - b) * v3.nz + b * v2.nz)

                p = Point3d(x, y, z, nx, ny, nz)
                p.normalize_normal()
                grid[(i, j)] = p

        triangles = []
        for i in range(subdivisions):
            for j in range(subdivisions):
                p0 = grid[(i, j)]
                p1 = grid[(i + 1, j)]
                p2 = grid[(i, j + 1)]
                p3 = grid[(i + 1, j + 1)]
                triangles.append((p0, p1, p2))
                triangles.append((p1, p3, p2))
        return triangles

    # --------------------------
    # GENERAL N-GON (fan subdivision)
    # --------------------------
    def _subdivide_ngon(self, vertices, subdivisions=1):
        """Subdivide an N-gon by triangulating into fans with normal interpolation."""
        triangles = []
        v0 = vertices[0]
        for i in range(1, len(vertices) - 1):
            v1 = vertices[i]
            v2 = vertices[i + 1]
            tris = self._subdivide_triangle(v0, v1, v2, subdivisions)
            triangles.extend(tris)
        return triangles

    # --------------------------
    # SPECIFIC CASES
    # --------------------------
    def subdivide_triangle(self, v0, v1, v2, subdivisions=1):
        return self._subdivide_triangle(v0, v1, v2, subdivisions)

    def subdivide_quad(self, v0, v1, v2, v3, subdivisions=1):
        return self._subdivide_quad(v0, v1, v2, v3, subdivisions)

    def subdivide_ngon(self, vertices, subdivisions=1):
        return self._subdivide_ngon(vertices, subdivisions)

    def subdivide_hexagon(self, vertices, subdivisions=1):
        return self._subdivide_ngon(vertices, subdivisions)

    def subdivide_octagon(self, vertices, subdivisions=1):
        return self._subdivide_ngon(vertices, subdivisions)

    def subdivide_prime_ngon(self, vertices, subdivisions=1):
        return self._subdivide_ngon(vertices, subdivisions)
