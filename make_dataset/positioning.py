import random


class Point:
    """Position of anything on the image with pixels"""

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __iter__(self):
        for attr in self.x, self.y:
            yield attr

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.x}, {self.y})'

    def shift(self, vertical: int, horizontal: int) -> 'Point':
        """Get new shifted position"""
        return Point(self.x + horizontal, self.y + vertical)


class Offset:
    """Offset from the position in pixels"""

    vertical: float
    horizontal: float

    @classmethod
    def random(cls, x_limit: int, y_limit: int):
        assert x_limit > 0 and y_limit > 0
        horizontal = random.randint(-x_limit, x_limit)
        vertical = random.randint(-y_limit, y_limit)

        return cls(vertical, horizontal)

    def __init__(self, vertical: float, horizontal: float) -> None:
        self.vertical = vertical
        self.horizontal = horizontal

    def __iter__(self):
        for attr in self.vertical, self.horizontal:
            yield attr

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}{tuple(self)}'

    def apply(self, x: int, y: int) -> tuple[float, float]:
        """Add the offset to a position"""
        return x + self.horizontal, y + self.vertical
