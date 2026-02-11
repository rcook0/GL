import matplotlib.pyplot as plt
from graphics_package.point3d import Point3d
from scene3d import Scene3d
from renderer import Renderer

def build_hexagon(radius=0.8, z=0.0):
    vertices = []
    for i in range(6):
        angle = 2 * 3.14159 * i / 6
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        vertices.append(Point3d(x, y, z, 0, 0, 1))  # upward normals
    return vertices

def main():
    width, height = 400, 400
    renderer = Renderer(width, height)
    scene = Scene3d(renderer)

    # Build and add hexagon
    hexagon = build_hexagon()
    scene.add_hexagon(hexagon, subdivisions=4)

    # Render scene
    img = scene.render(color=(0.2, 0.6, 1.0))

    # Show result
    plt.imshow(img)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    import numpy as np
    main()
