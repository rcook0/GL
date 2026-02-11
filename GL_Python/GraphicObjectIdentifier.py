class GraphicObjectIdentifier:
    def __init__(self, classname: str, obj: object):
        self.classname = classname
        self.obj = obj

    def getClassname(self) -> str:
        return self.classname

    def getObject(self):
        return self.obj

    def __str__(self) -> str:
        return f"GraphicObjectIdentifier({self.classname}, {self.obj})"
