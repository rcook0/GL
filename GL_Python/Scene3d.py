import numpy as np
from graphics_package.view3d import View3d
from graphics_package.igraphic_object3d import IGraphicObject3d
from graphics_package.transformation3d import Transformation3d
from graphics_package.line3d import Line3d
from graphics_package.polygon3d import Polygon3d
from graphics_package.mesh3d import Mesh3d
from graphics_package.vector4d import Vector4d
from graphics_package.point3d import Point3d
from graPHics_package.PolygonSubdivider import PolygonSubdivider

class Scene3d:
    def __init__(self, view=None):
        self.objects = []
        self.view = view if view is not None else View3d()
        self.lights = []  # placeholder for lighting models

    def __init__(self, renderer):
        self.renderer = renderer
        self.objects = []  # holds triangles for rendering
        self.subdivider = PolygonSubdivider()

    def add_object(self, obj: IGraphicObject3d):
        if not isinstance(obj, IGraphicObject3d):
            raise TypeError("Scene3d accepts only IGraphicObject3d")
        self.objects.append(obj)

 # --------------------------
    # Add general N-gons
    # --------------------------
    def add_ngon(self, vertices, subdivisions=1):
        """
        Accepts a list of Point3d vertices forming an N-gon,
        subdivides it into triangles, stores in scene.
        """
        tris = self.subdivider.subdivide_ngon(vertices, subdivisions)
        self.objects.extend(tris)

    def add_quad(self, v0, v1, v2, v3, subdivisions=1):
        tris = self.subdivider.subdivide_quad(v0, v1, v2, v3, subdivisions)
        self.objects.extend(tris)

    def add_triangle(self, v0, v1, v2, subdivisions=1):
        tris = self.subdivider.subdivide_triangle(v0, v1, v2, subdivisions)
        self.objects.extend(tris)

    def add_hexagon(self, vertices, subdivisions=1):
        tris = self.subdivider.subdivide_hexagon(vertices, subdivisions)
        self.objects.extend(tris)

    def add_octagon(self, vertices, subdivisions=1):
        tris = self.subdivider.subdivide_octagon(vertices, subdivisions)
        self.objects.extend(tris)

    def add_prime_ngon(self, vertices, subdivisions=1):
        tris = self.subdivider.subdivide_prime_ngon(vertices, subdivisions)
        self.objects.extend(tris)

    # --------------------------
    # Render
    # --------------------------
    def render(self, color=(1.0, 1.0, 1.0)):
        """Render the scene with backface culling + Phong shading."""
        self.renderer.clear()

        for tri in self.objects:
            v0, v1, v2 = tri

            # Backface culling
            n = self._compute_normal(v0, v1, v2)
            view_vec = np.array([0, 0, 1], dtype=np.float32)  # assume camera forward
            if np.dot(n, view_vec) <= 0:
                continue  # skip triangle

            # Render with per-vertex normals
            self.renderer.render_triangle(v0, v1, v2, color=color)

        return self.renderer.get_image()

    # --------------------------
    # Helpers
    # --------------------------
    def _compute_normal(self, v0, v1, v2):
        """Compute geometric normal of a triangle."""
        p0 = np.array([v0.x(), v0.y(), v0.z()])
        p1 = np.array([v1.x(), v1.y(), v1.z()])
        p2 = np.array([v2.x(), v2.y(), v2.z()])
        n = np.cross(p1 - p0, p2 - p0)
        norm = np.linalg.norm(n)
        if norm == 0:
            return np.array([0, 0, 1], dtype=np.float32)
        return n / norm
    
    def clear(self):
        self.objects.clear()

    def set_view(self, view: View3d):
        self.view = view

    def add_light(self, light):
        self.lights.append(light)

    def transform_all(self, matrix: Transformation3d):
        for obj in self.objects:
            obj.transform(matrix)

    def render(self):
        """
        Full pipeline:
          1. Normalize using perspective projection (view.nPer()).
          2. Clip lines/polygons against canonical view volume.
          3. Apply viewport transform (view.mVV3DV()).
          4. Back-face culling (for polygons).
          5. Painter’s Algorithm: sort polygons by avg z before projecting.
        Returns: list of Line2d
        """
        primitives = []

        # Build combined transformation
        nper = self.view.nPer()
        viewport = self.view.mVV3DV()
        pipeline = Transformation3d()
        pipeline.transform(nper)
        pipeline.transform(viewport)

        # View direction (camera looks down -Z in canonical space)
        view_dir = Vector4d(0, 0, -1, 0)

        # Collect polygons for painter’s algorithm
        polygon_list = []

        for obj in self.objects:
            if isinstance(obj, Line3d):
                if self.view.clip3d(obj, zmin=-1.0):
                    obj.transform(pipeline)
                    primitives.extend(obj.to_2d())
            elif isinstance(obj, Polygon3d):
                obj.transform(pipeline)
                if obj.is_front_facing(view_dir):
                    avg_z = sum(v.z() for v in obj.vertices) / len(obj.vertices)
                    polygon_list.append((avg_z, obj))
            elif isinstance(obj, Mesh3d):
                for poly in obj.polygons:
                    poly.transform(pipeline)
                    if poly.is_front_facing(view_dir):
                        avg_z = sum(v.z() for v in poly.vertices) / len(poly.vertices)
                        polygon_list.append((avg_z, poly))
            else:
                # Fallback for composites or other future IGraphicObject3d types
                obj.transform(pipeline)
                primitives.extend(obj.to_2d(view_dir=view_dir))

        # Sort polygons back-to-front
        polygon_list.sort(key=lambda tup: tup[0], reverse=True)

        # Project sorted polygons to 2D
        for _, poly in polygon_list:
            primitives.extend(poly.to_2d(view_dir=view_dir))

        return primitives

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        return iter(self.objects)

    def __str__(self):
        return f"Scene3d({len(self.objects)} objects, {len(self.lights)} lights)"
