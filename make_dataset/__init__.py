from typing import Sequence

from PIL import Image

from make_dataset.fields import Field
from make_dataset.render import FieldGroup

__version__ = '0.1.0'


class DocumentGenerator:
    """Create an image and render all fields on it"""

    groups: Sequence[FieldGroup]
    template: Image.Image

    @property
    def fields(self) -> list[Field]:
        return [
            field
            for group in self.groups
            for field in group.fields
        ]

    def __init__(
        self,
        template: Image.Image,
        groups: Sequence[FieldGroup],
    ) -> None:
        self.groups = groups
        self.template = template

    def generate(self) -> Image.Image:
        image = self.template

        for group in self.groups:
            image = group.render(image)

        return image
