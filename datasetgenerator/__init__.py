from typing import Sequence

from PIL import Image

from datasetgenerator.fields import Field, FieldGroup

__version__ = '0.1.0'


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
