# graphics_package/matrix.py
class Matrix:
    def __init__(self, rows, cols, val=0.0):
        self.rows = rows
        self.cols = cols
        self.m = [[val for _ in range(cols)] for _ in range(rows)]

    @classmethod
    def from_data(cls, data):
        rows = len(data)
        cols = len(data[0])
        for r in data:
            if len(r) != cols:
                raise ValueError("All rows must have the same length.")
        mat = cls(rows, cols, 0.0)
        mat.m = [list(r) for r in data]
        return mat

    def get_element(self, i, j):
        return self.m[i][j]

    def set_element(self, i, j, value):
        self.m[i][j] = value

    def mult(self, b: "Matrix") -> "Matrix":
        if self.rows != b.cols:
            raise ValueError("Matrices are not conformable.")
        result = Matrix(b.rows, self.cols, 0.0)
        for i in range(b.rows):
            for j in range(self.cols):
                s = 0.0
                for k in range(self.rows):
                    s += b.get_element(i, k) * self.m[k][j]
                result.m[i][j] = s
        return result

    def transform(self, b: "Matrix"):
        if self.rows != b.cols:
            raise ValueError("Matrices are not conformable.")
        result = [[0.0 for _ in range(self.cols)] for _ in range(b.rows)]
        for i in range(b.rows):
            for j in range(self.cols):
                s = 0.0
                for k in range(self.rows):
                    s += b.get_element(i, k) * self.m[k][j]
                result[i][j] = s
        self.m = result
        self.rows = b.rows

    def __str__(self):
        rows_str = []
        for row in self.m:
            rows_str.append("(" + ", ".join(f"{x:.3f}" for x in row) + ")")
        return "[" + "\n".join(rows_str) + "]"
