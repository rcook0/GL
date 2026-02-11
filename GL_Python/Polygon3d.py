# graphics_package/polygon3d.py
from graphics_package.point3d import Point3d
from graphics_package.line2d import Line2d
from graphics_package.igraphic_object3d import IGraphicObject3d
from graphics_package.vector4d import Vector4d

class Polygon3d(IGraphicObject3d):
    def __init__(self, *args):
        """
        Flexible constructor:
        - Polygon3D() → empty polygon
        - Polygon3D(p1, p2, p3, ...) → adds each Point3d
        - Polygon3D([p1, p2, p3]) → adds list of Point3d
        """
        self.vertices = []
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            for v in args[0]:
                self.add_vertex(v)
        elif len(args) > 0:
            for v in args:
                self.add_vertex(v)

    def add_vertex(self, v):
        # Expecting v to be Point3d
        self.vertices.append(v)

    def transform(self, matrix):
        self.vertices = [p.transform(matrix) for p in self.vertices]

    def normal(self):
        # Assume triangle for now
        if len(self.vertices) < 3:
            return None
        p0, p1, p2 = self.vertices[:3]
        u = np.array([p1.x - p0.x, p1.y - p0.y, p1.z - p0.z])
        v = np.array([p2.x - p0.x, p2.y - p0.y, p2.z - p0.z])
        n = np.cross(u, v)
        return n / np.linalg.norm(n)

    def is_front_facing(self, view_dir: Vector4d) -> bool:
        """Return True if polygon faces the viewer."""
        n = self.normal()
        dot = n.x() * view_dir.x() + n.y() * view_dir.y() + n.z() * view_dir.z()
        return dot < 0  # negative means facing camera

    def to_2d(self, view_dir=None):
        """Project to 2D edges, with optional back-face culling."""
        if view_dir is not None and not self.is_front_facing(view_dir):
            return []  # cull back-facing polygon

        lines = []
        if len(self.vertices) < 2:
            return lines

        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            lines.append(Line2d(p1.x(), p1.y(), p2.x(), p2.y()))
        return lines

    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices)

    def __str__(self):
        verts_str = ", ".join(str(v) for v in self.vertices)
        return f"Polygon3d({verts_str})"
