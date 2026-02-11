# graphics_package/Bezier2d.py
import math
from .Point2d import Point2d

class Bezier2d:
    """
    Python port of Bezier2d.
    Stores control points and evaluates the curve using Bernstein polynomials.
    """

    def __init__(self, parts: list[Point2d]):
        self.parts = parts[:]  # make a copy of the control points

    @staticmethod
    def fact(n: int) -> int:
        """Factorial n!"""
        return math.factorial(n)

    @staticmethod
    def choose(n: int, k: int) -> int:
        """Binomial coefficient nCk."""
        return math.comb(n, k)

    def bezier_point(self, t: float) -> Point2d:
        """
        Evaluate the Bezier curve at parameter t ∈ [0,1].

        Uses Bernstein polynomial basis.
        """
        n = len(self.parts) - 1
        x, y = 0.0, 0.0
        for i, pt in enumerate(self.parts):
            coeff = self.choose(n, i) * (t ** i) * ((1 - t) ** (n - i))
            x += coeff * pt.x()
            y += coeff * pt.y()
        return Point2d(x, y)

    def sample_curve(self, segments: int = 20) -> list[Point2d]:
        """
        Sample the Bezier curve into a list of points.

        Parameters
        ----------
        segments : int
            Number of line segments (more = smoother).

        Returns
        -------
        list[Point2d]
        """
        points = []
        for k in range(segments + 1):
            t = k / segments
            points.append(self.bezier_point(t))
        return points


"""
from typing import List, Tuple

def de_casteljau(ctrl: List[Tuple[float,float]], t: float) -> Tuple[float,float]:
    pts = [(float(x),float(y)) for x,y in ctrl]
    n = len(pts)
    for r in range(1, n):
        pts = [((1-t)*pts[i][0] + t*pts[i+1][0],
                (1-t)*pts[i][1] + t*pts[i+1][1]) for i in range(n-r)]
    return pts[0]

def sample(ctrl: List[Tuple[float,float]], segments: int = 10) -> List[Tuple[float,float]]:
    if not ctrl: return []
    if segments <= 0: return [ctrl[0], ctrl[-1]]
    dt = 1.0 / segments
    out = []
    t = 0.0
    for k in range(segments+1):
        out.append(de_casteljau(ctrl, t))
        t += dt
        if t > 1.0: t = 1.0
    return out
"""
