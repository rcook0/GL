# graphics_package/Buffer.py
import threading
import time
from .Drawing2d import Drawing2d
from .Point2d import Point2d

class Buffer:
    """
    Python port of Buffer (AWT/Swing-free).
    Manages animation updates and interaction state for a Drawing2d.
    """

    def __init__(self):
        self.myDrawing: Drawing2d | None = None
        self.running = False
        self.thread: threading.Thread | None = None

        # Interaction state
        self.click = False
        self.drag = False
        self.selectionPoint = Point2d(0.0, 0.0)

    def setDrawing(self, externalDrawing: Drawing2d) -> None:
        self.myDrawing = externalDrawing

    def getSelectionPoint(self) -> Point2d:
        self.click = False
        return self.selectionPoint

    def animateStart(self) -> None:
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def run(self) -> None:
        while self.running:
            self.update()
            time.sleep(0.05)

    def animateStop(self) -> None:
        self.running = False
        self.thread = None

    def update(self) -> None:
        """
        Perform one update cycle:
        draw + erase the drawing.
        """
        if self.myDrawing is None:
            self.myDrawing = Drawing2d()
        self.myDrawing.draw()
        self.myDrawing.erase()

    # --- Interaction emulation (mouse events) ---

    def click_event(self, x: float, y: float) -> None:
        if not self.click:
            self.selectionPoint = Point2d(x, y)
        self.click = True
        self.drag = False

    def release_event(self, x: float, y: float) -> None:
        self.drag = False

    def drag_event(self, x: float, y: float) -> None:
        self.drag = True
        self.selectionPoint = Point2d(x, y)

    def click_ack(self, ck: bool) -> None:
        self.click = ck

    def currentSelectionPointIsNew(self) -> bool:
        return self.click

    def dragging(self) -> bool:
        return self.drag
