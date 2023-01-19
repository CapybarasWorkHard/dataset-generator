from datasetgenerator.positioning import Point


class Field:
    """Editable document field"""

    name: str
    position: Point
    value: str

    def __init__(self, name: str, position: Point, value: str) -> None:
        self.name = name
        self.position = position
        self.value = value

    def __repr__(self) -> str:
        return f'{self.name}: \'{self.value}\' at {self.position}'
