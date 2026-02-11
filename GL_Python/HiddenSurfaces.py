"""Auto-translated skeleton from WINDOWS/Desktop/GraphicsPackage/HiddenSurfaces.java.
This file preserves classes, methods, and fields.
Bodies marked TODO.
"""
from __future__ import annotations
from typing import Any, Optional, List, Dict, Tuple, Iterable
import math

class HiddenSurfaces:
    def __init__(self):
        self.XMAX = None
        self.YMAX = None
        self.BACKGROUND_VALUE = None
        self.ZMIN = None
        self.ZMAX = None
        self.depthBuffer = None
        self.frameBuffer = None
        self.scans = None
        self.intersections = None
        self.pz = None
        self.scanline = None
        """TODO: Translate constructor body from Java."""
        pass

    def zBuffer(self):
        """TODO: Translate method body from Java."""
        raise NotImplementedError

    def for(self, polygon):
        """TODO: Translate method body from Java."""
        raise NotImplementedError

    def for(self, projection):
        """TODO: Translate method body from Java."""
        raise NotImplementedError

    def scan(self, polygon):
        """TODO: Translate method body from Java."""
        raise NotImplementedError

    def WritePixel(self, x, y, value):
        """TODO: Translate method body from Java."""
        raise NotImplementedError

    def ReadPixel(self, x, y):
        """TODO: Translate method body from Java."""
        raise NotImplementedError

    def WriteZ(self, x, y, value):
        """TODO: Translate method body from Java."""
        raise NotImplementedError

    def ReadZ(self, x, y):
        """TODO: Translate method body from Java."""
        raise NotImplementedError
