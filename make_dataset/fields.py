from make_dataset.positioning import Point


class Field:
    """Editable document field"""

    name: str
    point: Point
    value: str

    def __init__(self, name: str, point: Point, value: str) -> None:
        self.name = name
        self.point = point
        self.value = value

    def __repr__(self) -> str:
        return f'{self.name}: \'{self.value}\' at {self.point}'
