import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from point3d import Point3d
from polygon3d import Polygon3D
from scene3d import Scene3D

def rotation_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0.0],
                     [s,  c, 0.0],
                     [0.0,0.0,1.0]], dtype=float)

def project_ortho(p):
    # Simple orthographic projection: drop z
    return np.array([p.x(), p.y()], dtype=float)

def transform_point(p, R):
    v = np.array([p.x(), p.y(), p.z()], dtype=float)
    x, y, z = R @ v
    return Point3d(float(x), float(y), float(z))

def build_hexagon(r=0.8, z=0.0):
    verts = []
    for i in range(6):
        a = 2*np.pi*i/6.0
        verts.append(Point3d(r*np.cos(a), r*np.sin(a), z))
    return verts

def wire_segments(poly):
    # Return list of 2D segments [(x1,y1,x2,y2), ...]
    segs = []
    n = len(poly.vertices)
    for i in range(n):
        a = poly.vertices[i]
        b = poly.vertices[(i+1)%n]
        x1,y1 = project_ortho(a)
        x2,y2 = project_ortho(b)
        segs.append((x1,y1,x2,y2))
    return segs

def main():
    scene = Scene3D()
    hex_poly = Polygon3D(build_hexagon())
    # Subdivide to triangles for richer wireframe
    tris = hex_poly.subdivide_fan()
    for t in tris:
        scene.add_polygon(t)

    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_aspect('equal', 'box')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    lines = [ax.plot([], [], lw=1.0)[0] for _ in scene]

    def init():
        for ln in lines:
            ln.set_data([], [])
        return lines

    def update(frame):
        theta = frame * 0.05
        R = rotation_z(theta)
        for idx, poly in enumerate(scene):
            # transform vertices
            tverts = [transform_point(v, R) for v in poly.vertices]
            tpoly = Polygon3D(tverts)
            segs = wire_segments(tpoly)
            xs, ys = [], []
            for x1,y1,x2,y2 in segs:
                xs += [x1, x2, None]
                ys += [y1, y2, None]
            lines[idx].set_data(xs, ys)
        return lines

    ani = FuncAnimation(fig, update, init_func=init, frames=240, interval=30, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
