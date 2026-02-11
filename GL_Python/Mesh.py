# graphics_package/mesh3d.py
from graphics_package.igraphic_object3d import IGraphicObject3d
from graphics_package.polygon3d import Polygon3d

class Mesh3d(IGraphicObject3d):
    def __init__(self, polygons=None):
        """
        polygons: list of Polygon3d
        """
        self.polygons = polygons if polygons is not None else []

    def add_polygon(self, poly: Polygon3d):
        if not isinstance(poly, Polygon3d):
            raise TypeError("Mesh3d only accepts Polygon3d objects")
        self.polygons.append(poly)

    def transform(self, matrix):
        for poly in self.polygons:
            poly.transform(matrix)

    def to_2d(self):
        lines = []
        for poly in self.polygons:
            lines.extend(poly.to_2d())
        return lines

    def __len__(self):
        return len(self.polygons)

    def __iter__(self):
        return iter(self.polygons)

    def __str__(self):
        return f"Mesh3d({len(self.polygons)} polygons)"
