from graphics_package.scene3d import Scene3d
from graphics_package.mesh3d import Mesh3d
from graphics_package.polygon3d import Polygon3d
from graphics_package.point3d import Point3d

# Cube vertices
v = [
    Point3d(0,0,0), Point3d(1,0,0), Point3d(1,1,0), Point3d(0,1,0),
    Point3d(0,0,1), Point3d(1,0,1), Point3d(1,1,1), Point3d(0,1,1)
]

# Cube faces
faces = [
    Polygon3d([v[0], v[1], v[2], v[3]]),
    Polygon3d([v[4], v[5], v[6], v[7]]),
    Polygon3d([v[0], v[1], v[5], v[4]]),
    Polygon3d([v[2], v[3], v[7], v[6]]),
    Polygon3d([v[1], v[2], v[6], v[5]]),
    Polygon3d([v[0], v[3], v[7], v[4]])
]

cube = Mesh3d(faces)
scene = Scene3d()
scene.add_object(cube)

edges = scene.render()
for e in edges:
    print(e)
