# graphics_package/RadianSinLookup.py
import math

class RadianSinLookup:
    """
    Python port of RadianSinLookup.
    Provides a sine lookup table and utility conversions.
    """

    def __init__(self, steps: int = 360):
        """
        Initialize the sine lookup table.

        Parameters
        ----------
        steps : int
            Number of steps per circle (default 360 = 1 degree resolution).
        """
        self.steps = steps
        self.table = [math.sin(2 * math.pi * i / steps) for i in range(steps)]

    def radian_angle_of(self, degrees: float) -> float:
        """
        Convert degrees to radians.
        """
        return math.radians(degrees)

    def radians(self, degrees: float) -> float:
        """
        Alias for radian_angle_of.
        """
        return self.radian_angle_of(degrees)

    def radians_to_degrees(self, radians: float) -> float:
        """
        Convert radians to degrees.
        """
        return math.degrees(radians)

    def trig_sin(self, radians: float) -> float:
        """
        Approximate sine using lookup table.

        Parameters
        ----------
        radians : float
            Angle in radians.

        Returns
        -------
        float
            Approximated sine value.
        """
        index = int((radians % (2 * math.pi)) / (2 * math.pi) * self.steps)
        return self.table[index]
