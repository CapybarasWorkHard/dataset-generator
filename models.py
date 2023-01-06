import random


class Field:
    """Editable document field"""

    name: str
    position: 'Position'
    offset: 'Offset'

    @property
    def normalized_position(self) -> tuple[int, int]:
        """Get offseted position and normalize it"""
        position = self.offset.apply(self.position.x, self.position.y)
        return tuple(map(int, position))

    def __init__(self, name: str, position: 'Position', offset: 'Offset') -> None:
        self.name = name
        self.position = position
        self.offset = offset


class Position:
    """Position of anything on the image with pixels"""

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Offset:
    """Offset from the position in pixels"""

    vertical: float
    horizontal: float

    def __init__(self, vertical: float, horizontal: float) -> None:
        self.vertical = vertical
        self.horizontal = horizontal

    @classmethod
    def random(cls, x_limit: int, y_limit: int):
        vertical = random.randint(-x_limit, x_limit)
        horizontal = random.randint(-y_limit, y_limit)

        return cls(vertical, horizontal)

    def apply(self, x: int, y: int) -> tuple[float, float]:
        """Add the offset to a position"""
        return x + self.horizontal, y + self.vertical
