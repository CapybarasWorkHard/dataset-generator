from dataclasses import dataclass
import random


@dataclass
class Point:
    """Position of anything on the image with pixels"""

    x: int
    y: int

    def __iter__(self):
        yield from (self.x, self.y)

    def shift(self, vertical: int, horizontal: int) -> 'Point':
        """Get new shifted position"""
        return Point(self.x + horizontal, self.y + vertical)


@dataclass
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

    def __iter__(self):
        yield from (self.vertical, self.horizontal)

    def apply(self, x: int, y: int) -> tuple[float, float]:
        """Add the offset to a position"""
        return x + self.horizontal, y + self.vertical
