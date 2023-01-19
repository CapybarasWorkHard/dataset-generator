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
