from typing import Callable

from datasetgenerator.factories import Factory
from datasetgenerator.fields import Field
from datasetgenerator.positioning import Offset, Point


class FieldFactory(Factory[Field]):
    """Generate field with random padding and value"""

    name: str
    offset_limit: tuple[int, int]
    point: Point
    value_function: Callable[[], str]

    def __init__(
        self,
        name: str,
        point: Point,
        value_function: Callable[[], str],
        offset_limit: tuple[int, int] | None = None,
    ) -> None:
        self.name = name
        self.offset_limit = offset_limit or (0, 0)
        self.point = point
        self.value_function = value_function

    def create(self) -> Field:
        position = self._shift_position()
        value = self.value_function()

        return Field(self.name, position, value)

    def _shift_position(self):
        x, y = self.offset_limit

        if not x or not y:
            return self.point

        offset = Offset.random(x, y)
        vertical, horizontal = map(int, offset)

        return self.point.shift(vertical, horizontal)
