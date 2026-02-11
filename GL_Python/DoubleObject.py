# graphics_package/DoubleObject.py
class DoubleObject:
    """
    Wrapper around a float, mirroring the Java DoubleObject.
    """

    def __init__(self, value: float = 0.0):
        self.value = float(value)

    def get(self) -> float:
        return self.value

    def set(self, v: float) -> None:
        self.value = float(v)

    def __str__(self) -> str:
        return str(self.value)

    def __float__(self) -> float:
        return self.value
