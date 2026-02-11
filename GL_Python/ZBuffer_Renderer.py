# graphics_package/zbuffer_renderer.py
import numpy as np
import matplotlib.pyplot as plt
from graphics_package.scene3d import Scene3d
from graphics_package.polygon3d import Polygon3d
from graphics_package.point3d import Point3d


class ZBufferRenderer:
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height
        self.color_buffer = np.zeros((height, width, 3), dtype=np.float32)  # RGB
        self.z_buffer = np.full((height, width), np.inf)  # depth values

    def clear(self):
        self.color_buffer.fill(0.0)
        self.z_buffer.fill(np.inf)

    def render_scene(self, scene: Scene3d, subdiv=1, backface_culling=True):
        """
        Rasterize polygons from a Scene3d using z-buffer hidden-surface elimination.
        Tessellates polygons to triangles, applies backface culling, then rasterizes.
        """
        for poly in scene.objects:
            if isinstance(poly, Polygon3d):
                triangles = poly.triangulate(subdiv=subdiv)

                for tri in triangles:
                    if backface_culling and self.is_backfacing(tri):
                        continue  # skip invisible triangles
                    self._rasterize_triangle(tri)

    # ------------------------------
    # Geometry helpers
    # ------------------------------

    def is_backfacing(self, tri: Polygon3d, view_dir=(0, 0, -1)):
        """
        Return True if the triangle is backfacing relative to the view direction.
        Assumes vertices are already in view space (camera looks down -Z).
        """
        v0, v1, v2 = tri.vertices
        e1 = np.array([v1.x() - v0.x(), v1.y() - v0.y(), v1.z() - v0.z()])
        e2 = np.array([v2.x() - v0.x(), v2.y() - v0.y(), v2.z() - v0.z()])
        normal = np.cross(e1, e2)

        view = np.array(view_dir)
        return np.dot(normal, view) >= 0  # >=0 → backfacing

    # ------------------------------
    # Triangle rasterizer
    # ------------------------------

    def _rasterize_triangle(self, tri: Polygon3d, color=(1.0, 1.0, 1.0)):
        """
        Fill a triangle using barycentric interpolation + z-buffer test.
        """
        verts = [(int(v.x()), int(v.y()), v.z()) for v in tri.vertices]
        (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = verts

        # Bounding box
        min_x, max_x = max(min(x0, x1, x2), 0), min(max(x0, x1, x2), self.width - 1)
        min_y, max_y = max(min(y0, y1, y2), 0), min(max(y0, y1, y2), self.height - 1)

        # Edge function
        def edge(xa, ya, xb, yb, xc, yc):
            return (xc - xa) * (yb - ya) - (yc - ya) * (xb - xa)

        area = edge(x0, y0, x1, y1, x2, y2)
        if area == 0:
            return  # degenerate

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                w0 = edge(x1, y1, x2, y2, x, y)
                w1 = edge(x2, y2, x0, y0, x, y)
                w2 = edge(x0, y0, x1, y1, x, y)

                if (w0 >= 0 and w1 >= 0 and w2 >= 0) or (w0 <= 0 and w1 <= 0 and w2 <= 0):
                    # Barycentric interpolation
                    alpha = w0 / area
                    beta = w1 / area
                    gamma = w2 / area

                    z = alpha * z0 + beta * z1 + gamma * z2

                    if z < self.z_buffer[y, x]:
                        self.z_buffer[y, x] = z
                        self.color_buffer[y, x] = color

    def show(self):
        plt.imshow(self.color_buffer, origin="lower")
        plt.axis("off")
        plt.show()
