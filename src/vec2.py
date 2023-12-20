import math

class Vec2:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    # rotating a vector v by a:
    # x = v.x * cos(a) - v.y * sin(a)
    # y = v.x * sin(a) + v.y * cos(a)
    def rotate(self, rad) -> None:
        x = self.x * math.cos(rad) - self.y * math.sin(rad)
        y = self.x * math.sin(rad) + self.y * math.cos(rad)
        self.x = x
        self.y = y

    def add(self, vec) -> None:
        self.x += vec.x
        self.y += vec.y

    def scale(self, val) -> None:
        self.x *= val
        self.y += val

    def get_length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def to_ivec2(self) -> None:
        self.x = int(self.x)
        self.y = int(self.y)

    def __str__(self) -> str:
        return f"vec2[{self.x}, {self.y}]"

