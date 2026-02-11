# graphics_package/Input.py
class Input:
    """
    Minimal Input utility to wrap Python's input().
    """

    @staticmethod
    def read_line(prompt: str = "") -> str:
        return input(prompt)

    @staticmethod
    def read_int(prompt: str = "") -> int:
        return int(input(prompt))

    @staticmethod
    def read_float(prompt: str = "") -> float:
        return float(input(prompt))
