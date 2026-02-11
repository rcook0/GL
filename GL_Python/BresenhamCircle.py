
from typing import List, Tuple

class BresenhamCircle:
    """
    Python port of BresenhamCircle.
    Uses the midpoint circle algorithm to generate 8-way symmetric points.
    """

    def __init__(self, cx: int, cy: int, r: int):
        self.cx = cx
        self.cy = cy
        self.r = r

    def rasterize(cx: int, cy: int, r: int) -> List[Tuple[int,int]]:
        """
        Generate the circle raster points.

        Returns
        -------
        List[Tuple[int, int]]
            List of (x,y) integer coordinates on the circle.
        """
        cx, cy, r = self.cx, self.cy, self.r
        x, y = 0, r
        d = 1 - r
        pts: List[Tuple[int, int]] = []

    
        def emit(a: int, b: int) -> None:
            pts.extend([
                (cx + a, cy + b),
                (cx + b, cy + a),
                (cx - a, cy + b),
                (cx - b, cy + a),
                (cx + a, cy - b),
                (cx + b, cy - a),
                (cx - a, cy - b),
                (cx - b, cy - a),
            ])
        
        emit(x,y)
        while x < y:
            if d < 0:
                d += 2*x + 3
            else:
                d += 2*(x - y) + 5
                y -= 1
            x += 1
            emit(x,y)
    
        # Remove duplicates and sort for consistency
        return sorted(set(pts))
