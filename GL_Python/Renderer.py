import numpy as np
from graphics_package.point3d import Point3d

class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color_buffer = np.zeros((height, width, 3), dtype=np.float32)
        self.depth_buffer = np.full((height, width), np.inf, dtype=np.float32)

        # simple directional light
        self.light_dir = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.light_dir /= np.linalg.norm(self.light_dir)

        # camera position for specular term
        self.camera_pos = np.array([0.0, 0.0, 10.0], dtype=np.float32)

    def clear(self, color=(0.0, 0.0, 0.0)):
        self.color_buffer[:] = color
        self.depth_buffer[:] = np.inf

    def render_triangle(self, v0: Point3d, v1: Point3d, v2: Point3d, color=(1.0, 1.0, 1.0)):
        """Rasterize a triangle with Phong shading and depth buffering."""

        # Project to screen space (simple orthographic for now)
        pts = []
        for v in (v0, v1, v2):
            sx = int((v.x() + 1) * 0.5 * (self.width - 1))
            sy = int((1 - (v.y() + 1) * 0.5) * (self.height - 1))
            pts.append((sx, sy, v.z(), np.array([v.nx, v.ny, v.nz], dtype=np.float32)))

        (x0, y0, z0, n0), (x1, y1, z1, n1), (x2, y2, z2, n2) = pts

        # Bounding box
        min_x = max(min(x0, x1, x2), 0)
        max_x = min(max(x0, x1, x2), self.width - 1)
        min_y = max(min(y0, y1, y2), 0)
        max_y = min(max(y0, y1, y2), self.height - 1)

        # Edge function
        def edge(ax, ay, bx, by, cx, cy):
            return (cx - ax) * (by - ay) - (cy - ay) * (bx - ax)

        area = edge(x0, y0, x1, y1, x2, y2)
        if area == 0:
            return

        # Rasterize
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                w0 = edge(x1, y1, x2, y2, x, y)
                w1 = edge(x2, y2, x0, y0, x, y)
                w2 = edge(x0, y0, x1, y1, x, y)
                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    # barycentric
                    w0 /= area
                    w1 /= area
                    w2 /= area

                    z = w0 * z0 + w1 * z1 + w2 * z2
                    if z < self.depth_buffer[y, x]:
                        # interpolate normals
                        n = w0 * n0 + w1 * n1 + w2 * n2
                        n /= np.linalg.norm(n) + 1e-8

                        # Phong lighting
                        intensity = self._phong_shade(n)
                        shaded = np.clip(np.array(color) * intensity, 0, 1)

                        self.color_buffer[y, x] = shaded
                        self.depth_buffer[y, x] = z

    def _phong_shade(self, n):
        """Return light intensity using Phong model."""
        # ambient
        Ia = 0.1
        # diffuse
        L = self.light_dir
        Id = max(np.dot(n, -L), 0.0)
        # specular
        V = np.array([0, 0, 1], dtype=np.float32)  # assume screen-facing camera
        R = 2 * np.dot(n, -L) * n - (-L)
        Is = max(np.dot(R, V), 0.0) ** 16  # shininess

        return Ia + 0.7 * Id + 0.2 * Is

    def get_image(self):
        """Return the image buffer as uint8 RGB."""
        return np.clip(self.color_buffer * 255, 0, 255).astype(np.uint8)
