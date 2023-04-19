import random
from dataclasses import dataclass


@dataclass
class Point:
    """Position of anything on the image with pixels"""

    x: int
    y: int

    def __iter__(self):
        yield from (self.x, self.y)

    def shift(self, vertical: int, horizontal: int) -> 'Point':
        """Get new shifted position"""
        return Point(self.x + vertical, self.y + horizontal)


@dataclass
class Offset:
    """Offset from the position in pixels"""

    vertical: float
    horizontal: float

    @classmethod
    def random(cls, x: int, y: int) -> 'Offset':
        assert x > 0 and y > 0, 'Values should be greater than zero'
        horizontal = random.randint(-x, x)
        vertical = random.randint(-y, y)

        return cls(vertical, horizontal)

    def __iter__(self):
        yield from (self.vertical, self.horizontal)

    def apply(self, x: int, y: int) -> tuple[float, float]:
        """Add the offset to a position"""
        return x + self.horizontal, y + self.vertical
