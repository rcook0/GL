from graphics_package.point3d import Point3d
from graphics_package.polygon3d import Polygon3d
from graphics_package.mesh3d import Mesh3d

# Define cube vertices
v = [
    Point3d(0,0,0), Point3d(1,0,0), Point3d(1,1,0), Point3d(0,1,0),  # bottom face
    Point3d(0,0,1), Point3d(1,0,1), Point3d(1,1,1), Point3d(0,1,1)   # top face
]

# Define 6 cube faces (as polygons)
faces = [
    Polygon3d([v[0], v[1], v[2], v[3]]),  # bottom
    Polygon3d([v[4], v[5], v[6], v[7]]),  # top
    Polygon3d([v[0], v[1], v[5], v[4]]),  # front
    Polygon3d([v[2], v[3], v[7], v[6]]),  # back
    Polygon3d([v[1], v[2], v[6], v[5]]),  # right
    Polygon3d([v[0], v[3], v[7], v[4]]),  # left
]

cube = Mesh3d(faces)

# Project cube to 2D
edges = cube.to_2d()
for e in edges:
    print(e)
