from typing import Callable

from models import Factory, Field, Offset, Position


class FieldFactory(Factory[Field]):
    name: str
    offset_limit: tuple[int, int]
    position: Position
    value_function: Callable[[], str]

    def __init__(
        self,
        name: str,
        position: Position,
        value_function: Callable[[], str],
        offset_limit: tuple[int, int] | None = None,
    ) -> None:
        self.name = name
        self.offset_limit = offset_limit or (0, 0)
        self.position = position
        self.value_function = value_function

    def create(self) -> Field:
        """Create random field"""
        position = self._get_position()
        value = self.value_function()

        return Field(self.name, position, value)

    def _get_position(self):
        x, y = self.offset_limit

        if not x or not y:
            return self.position

        offset = Offset.random(x, y)
        vertical, horizontal = int(offset.vertical), int(offset.horizontal)

        return self.position.shift(vertical, horizontal)
