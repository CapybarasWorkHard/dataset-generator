from typing import Sequence

from PIL import Image

from datasetgenerator.factories import Factory
from datasetgenerator.positioning import Point
from datasetgenerator.rendering import Renderer


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


class FieldGroup:
    """Multiple fields designed to the same display way"""

    data: Sequence[Field | Factory[Field]]
    fields: Sequence[Field]
    renderer: Renderer

    def __init__(
        self,
        renderer: Renderer,
        data: Sequence[Field | Factory[Field]],
    ) -> None:
        self.data = data
        self.renderer = renderer

    def __len__(self) -> int:
        return len(self.fields)

    def render(self, image: Image.Image) -> Image.Image:
        self.seed()
        return self.renderer.render(image, self.fields)

    def seed(self) -> None:
        """regenerate fields by factories if any"""
        self.fields = [
            item.create() if isinstance(item, Factory) else item
            for item in self.data
        ]
