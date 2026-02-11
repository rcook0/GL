# graphics_package/IntegerObject.py
class IntegerObject:
    """
    Wrapper around an int, mirroring the Java IntegerObject.
    """

    def __init__(self, value: int = 0):
        self.value = int(value)

    def get(self) -> int:
        return self.value

    def set(self, v: int) -> None:
        self.value = int(v)

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value
