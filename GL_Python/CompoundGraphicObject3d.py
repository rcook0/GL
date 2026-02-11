from graphics_package.igraphic_object3d import IGraphicObject3d

class CompoundGraphicObject3d(IGraphicObject3d):
    def __init__(self):
        self.objects = []

    def add(self, obj: IGraphicObject3d):
        if not isinstance(obj, IGraphicObject3d):
            raise TypeError("CompoundGraphicObject3d accepts only IGraphicObject3d")
        self.objects.append(obj)

    def clear(self):
        self.objects.clear()

    def transform(self, matrix):
        for obj in self.objects:
            obj.transform(matrix)

    def to_2d(self):
        primitives = []
        for obj in self.objects:
            primitives.extend(obj.to_2d())
        return primitives

    def __iter__(self):
        return iter(self.objects)

    def __len__(self):
        return len(self.objects)

    def __str__(self):
        return f"CompoundGraphicObject3d({len(self.objects)} objects)"
