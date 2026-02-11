# graphics_package/ForeignObjectException.py

class ForeignObjectException(Exception):
    """
    Raised when a CompoundGraphicObject2d or related graph
    encounters an unknown or unsupported artifact.
    """
    def __init__(self, message: str, offending_object=None):
        super().__init__(message)
        self.offending_object = offending_object
