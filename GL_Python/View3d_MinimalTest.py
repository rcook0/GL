# graphics_package/View3dTest.py
import matplotlib.pyplot as plt
from .Point3d import Point3d
from .Line3d import Line3d
from .View3d import View3d
from .Transformation3d import Transformation3d

class View3dTest:
    def __init__(self):
        self.lines = []
        self.view = View3d()
        self.geom()

    def geom(self):
        a = Point3d(0, 0, 1)
        b = Point3d(0, 1, 0)
        c = Point3d(0, 1, 1)
        d = Point3d(1, 0, 0)
        e = Point3d(1, 0, 1)
        f = Point3d(1, 1, 0)
        g = Point3d(1, 1, 1)
        h = Point3d(0, 0, 0)
        cube = [a, b, c, d, e, f, g, h]

        shift = Transformation3d(); shift.translate(-0.5, -0.5, -0.5)
        scale = Transformation3d(); scale.scale(2, 2, 2)

        for p in cube:
            p.transform(shift); p.transform(scale); p.transform(self.view.nPer())

        self.lines = [
            Line3d(a, c), Line3d(c, g), Line3d(g, e), Line3d(e, a),
            Line3d(h, d), Line3d(d, f), Line3d(f, b), Line3d(b, h),
            Line3d(f, g), Line3d(b, c), Line3d(d, e), Line3d(h, a)
        ]

    def processViewingOp_PER(self):
        results = []
        for i, line in enumerate(self.lines):
            if self.view.clip3d(line, 1.3333):
                nper = self.view.nPer()
                vv = self.view.mVV3DV()
                src, dst = line.getSourcePoint(), line.getDestinationPoint()
                src.transform(nper); dst.transform(nper)
                src.transform(vv); dst.transform(vv)
                results.append(line)
            else:
                results.append(None)
        return results

    def run(self, plot=True):
        self.geom()
        lines2d = self.processViewingOp_PER()

        if plot:
            fig, ax = plt.subplots()
            for l in lines2d:
                if l:
                    p0, p1 = l.getSourcePoint(), l.getDestinationPoint()
                    ax.plot([p0.x(), p1.x()], [p0.y(), p1.y()], "k-")
            ax.set_aspect("equal", "box")
            ax.set_title("Projected Cube (View3dTest)")
            plt.show()

        return lines2d

if __name__ == "__main__":
    View3dTest().run(plot=True)
