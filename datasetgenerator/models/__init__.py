from typing import Sequence

from PIL import Image

from datasetgenerator.factories import Factory
from datasetgenerator.fields import Field
from datasetgenerator.rendering import Renderer


class DocumentGenerator:
    """Create an image and render all fields on it"""

    groups: Sequence['FieldGroup']
    image: Image.Image

    @property
    def fields(self) -> list['Field']:
        return [
            field
            for group in self.groups
            for field in group.fields
        ]

    def __init__(
        self,
        image: Image.Image,
        groups: Sequence['FieldGroup'],
    ) -> None:
        self.groups = groups
        self.image = image

    def generate(self) -> Image.Image:
        image = self.image

        for renderer in self.groups:
            image = renderer.render(image)

        return image


class FieldGroup:
    """Multiple fields designed to the same display way"""

    data: Sequence[Field | Factory[Field]]
    fields: Sequence[Field]
    renderer: 'Renderer'

    def __init__(
        self,
        renderer: 'Renderer',
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
