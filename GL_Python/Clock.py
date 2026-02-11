
import math, datetime, time
from .ApplicationFrame import ApplicationFrame
from .Transformation2d import Transformation2d
from .CompoundGraphicObject2d import CompoundGraphicObject2d
from .Point2d import Point2d
from .Line2d import Line2d
from .Widget2d import Widget2d
from .Numeral import Numeral
from .BresenhamCircle import BresenhamCircle
from .Bezier2dGO import Bezier2dGO

class Clock(ApplicationFrame):
    CLOCK_12 = 12
    CLOCK_24 = 24

    NORMAL_HZ = 2     # regular operation update frequency
    DRAG_HZ   = 60    # update frequency when dragging a widget

    def __init__(self):
        super().__init__()
        self.myTrans = Transformation2d()
        self.dynGeom = CompoundGraphicObject2d()

        self.mainFaceCentre = Point2d(200, 170)
        self.faceRadius = 150
        self.numeralRadius = 0
        self.chronoHandRadius = 0

        self.handWidthHour = 12
        self.handWidthMinute = 8
        self.handWidthSecond = 3

        self.currentTimeMinutes = 0
        self.currentTimeSeconds = 0
        self.currentTimeHours = 0

        self.minuteHandSelect = False
        self.hourHandSelect = False
        self.secondHandSelect = False

        self.sweepSecondValue = 0
        self.hourTotaliserValue = 0
        self.minuteTotaliserValue = 0

        self.minTotC = Point2d(0.0, 0.0)
        self.hourTotC = Point2d(0.0, 0.0)
        self.sweepSecC = Point2d(0.0, 0.0)

        self.CLOCK_TYPE = Clock.CLOCK_12

        self._init_static()

    def _init_static(self):
        self.setSize((400, 400))

        self.mainFaceCentre = Point2d(self.getSize().getWidth()/2, self.getSize().getHeight()/2 - 30)
        irRadius = 150
        self.faceRadius = irRadius
        orRadius = int(1.125*irRadius)
        self.numeralRadius = int(0.9*irRadius)

        self.minTotC = Point2d(self.mainFaceCentre.x()+(0.5*self.faceRadius), self.mainFaceCentre.y())
        self.hourTotC = Point2d(self.mainFaceCentre.x()-(0.5*self.faceRadius), self.mainFaceCentre.y())
        self.sweepSecC = Point2d(self.mainFaceCentre.x(), self.mainFaceCentre.y()+(0.5*self.faceRadius))
        totaliserRadius = int(0.25*self.faceRadius)
        self.chronoHandRadius = int(0.8*totaliserRadius)

        clock = CompoundGraphicObject2d()
        face = CompoundGraphicObject2d()
        hub = CompoundGraphicObject2d()
        rim = CompoundGraphicObject2d()
        numerals = CompoundGraphicObject2d()

        face.add(self.dynGeom)

        self.myDrawing.add(clock)
        clock.add(face)
        face.add(BresenhamCircle(self.mainFaceCentre, self.faceRadius))
        rim.add(BresenhamCircle(self.mainFaceCentre, orRadius))
        rim.add(BresenhamCircle(self.mainFaceCentre, irRadius))
        face.add(rim)
        face.add(hub)
        hub.add(BresenhamCircle(self.mainFaceCentre, self.numeralRadius//12))
        hub.add(BresenhamCircle(self.mainFaceCentre, self.numeralRadius//18))
        hub.add(BresenhamCircle(self.mainFaceCentre, self.numeralRadius//24))

        face.add(BresenhamCircle(self.minTotC, totaliserRadius))
        face.add(BresenhamCircle(self.hourTotC, totaliserRadius))
        face.add(BresenhamCircle(self.sweepSecC, totaliserRadius))

        toOrigin = Transformation2d()
        rotation = Transformation2d()
        toPos = Transformation2d()
        toOrigin.translate(-self.mainFaceCentre.x(), -self.mainFaceCentre.y())
        rotation.rotate(math.pi/6)
        toPos.translate(self.mainFaceCentre.x(), self.mainFaceCentre.y())
        drawNumerals = Transformation2d()
        drawNumerals.transform(toOrigin)
        drawNumerals.transform(rotation)
        drawNumerals.transform(toPos)

        centre = self.mainFaceCentre
        line = Line2d(centre.x(), centre.y(), centre.x(), centre.y() - self.numeralRadius)

        for i in range(12, 0, -1):
            pt = line.getDestinationPoint()
            numerals.add(Numeral(self._toChar(i), pt))
            line.transform(drawNumerals)

        face.add(numerals)

    def _toChar(self, i: int) -> str:
        return str(i)

    def updatePicture(self):
        now = datetime.datetime.now()
        self.currentTimeSeconds = now.second
        self.currentTimeMinutes = now.minute
        self.currentTimeHours = now.hour if self.CLOCK_TYPE == Clock.CLOCK_24 else (now.hour % 12)

        secHand = CompoundGraphicObject2d()
        minHand = CompoundGraphicObject2d()
        hourHand = CompoundGraphicObject2d()

        secondHandLength = int(0.9 * self.faceRadius)
        minuteHandLength = int(0.9 * self.faceRadius)
        hourHandLength   = int(0.6 * self.faceRadius)

        secondHandWidget = Widget2d(Point2d(self.mainFaceCentre.x(), self.mainFaceCentre.y()-secondHandLength), (20,20), True, secHand)
        minuteHandWidget = Widget2d(Point2d(self.mainFaceCentre.x(), self.mainFaceCentre.y()-minuteHandLength), (20,20), True, minHand)
        hourHandWidget   = Widget2d(Point2d(self.mainFaceCentre.x(), self.mainFaceCentre.y()-hourHandLength),   (20,20), True, hourHand)

        if self.secondHandSelect: secondHandWidget.select()
        if self.minuteHandSelect: minuteHandWidget.select()
        if self.hourHandSelect:   hourHandWidget.select()

        def add_hand(comp, length, width, widget):
            comp.add(Line2d(self.mainFaceCentre.x(), self.mainFaceCentre.y(),
                            self.mainFaceCentre.x(), self.mainFaceCentre.y() - length))
            comp.add(widget)
            base = self.mainFaceCentre
            tip = Point2d(base.x(), base.y() - length)
            left_ctrl  = Point2d(base.x() - width, base.y() - length/2)
            right_ctrl = Point2d(base.x() + width, base.y() - length/2)
            comp.add(Bezier2dGO([base, left_ctrl, tip], steps=30))
            comp.add(Bezier2dGO([base, right_ctrl, tip], steps=30))

        add_hand(secHand, secondHandLength, self.handWidthSecond, secondHandWidget)
        add_hand(minHand, minuteHandLength, self.handWidthMinute, minuteHandWidget)
        add_hand(hourHand, hourHandLength, self.handWidthHour, hourHandWidget)

        secondsAngle = -math.pi*2*self.currentTimeSeconds/60.0
        minutesAngle = -math.pi*2*self.currentTimeMinutes/60.0
        hoursAngle   = -math.pi*2*(self.currentTimeHours % 12)/12.0

        if self.myBuffer.dragging():
            selPoint = self.myBuffer.getSelectionPoint()
            selPoint = Point2d(selPoint.x(), self.getHeight() - selPoint.y())
            centre = Point2d(self.mainFaceCentre.x(), self.getHeight() - self.mainFaceCentre.y())
            if self.secondHandSelect:
                secondsAngle = -Widget2d.angleOfRotation(centre, selPoint)
            if self.minuteHandSelect:
                minutesAngle = -Widget2d.angleOfRotation(centre, selPoint)
            if self.hourHandSelect:
                hoursAngle = -Widget2d.angleOfRotation(centre, selPoint)

        def rotate_about_center(angle):
            t = Transformation2d(); t1 = Transformation2d(); t2 = Transformation2d()
            t1.translate(-self.mainFaceCentre.x(), -self.mainFaceCentre.y())
            t2.translate(self.mainFaceCentre.x(), self.mainFaceCentre.y())
            r = Transformation2d(); r.rotate(angle)
            t.transform(t1); t.transform(r); t.transform(t2)
            return t

        secHand.transform(rotate_about_center(secondsAngle))
        minHand.transform(rotate_about_center(minutesAngle))
        hourHand.transform(rotate_about_center(hoursAngle))

        if self.myBuffer.currentSelectionPointIsNew() and (not self.myBuffer.dragging()):
            selPoint = self.myBuffer.getSelectionPoint()
            self.secondHandSelect = secondHandWidget.hasPoint(int(selPoint.x()), int(selPoint.y()))
            self.minuteHandSelect = minuteHandWidget.hasPoint(int(selPoint.x()), int(selPoint.y()))
            self.hourHandSelect   = hourHandWidget.hasPoint(int(selPoint.x()), int(selPoint.y()))

        newHandState = CompoundGraphicObject2d()
        newHandState.add(secHand)
        newHandState.add(minHand)
        newHandState.add(hourHand)

        self.dynGeom.clear()
        self.dynGeom.add(newHandState)

    def initComponents(self):
        super().initComponents()
        self.setBackground("white")
        self.setLocation((200, 150))
        self.setTitle("Analog Clock")
        self.setVisible(True)

class MainMenu: pass

def main():
    frame = Clock()
    frame.setMainMenu(MainMenu())
    frame.initComponents()
        """
        for _ in range(5):
            frame.updatePicture()
        """
    while True:
        frame.updatePicture()
        if frame.myBuffer.dragging():
            time.sleep(1.0 / frame.DRAG_HZ)
        else:
            time.sleep(1.0 / frame.NORMAL_HZ)
