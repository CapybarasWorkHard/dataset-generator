from pathlib import Path
from typing import Generic, Literal, Sequence, TypeAlias, TypeVar

from PIL import Image, ImageDraw, ImageFont

from datasetgenerator.fields import Field

_Color: TypeAlias = int | str | tuple[int, ...]
_InstanceType = TypeVar('_InstanceType')


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


class Factory(Generic[_InstanceType]):
    """Allows you to dynamically create classes"""

    def create(self) -> _InstanceType:
        raise NotImplementedError()


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


class Font:
    """Font display settings"""

    align: Literal['center', 'left', 'right']
    anchor: str
    color: _Color
    file: str
    size: int
    spacing: float

    @property
    def pil_font(self) -> ImageFont.FreeTypeFont:
        """Get Pillow ImageFont object"""
        return ImageFont.truetype(self.file, self.size)

    def __init__(
        self,
        color: _Color,
        file: str | Path,
        size: int,
        anchor: str = 'lt',
    ) -> None:
        self.anchor = anchor
        self.color = color
        self.file = str(file.resolve()) if isinstance(file, Path) else file
        self.size = size

    def __repr__(self) -> str:
        font_name = self.pil_font.getname()
        return f'{font_name} {self.size}. {self.color}'

    def draw(
        self,
        overlay: ImageDraw.ImageDraw,
        position: tuple[float, float],
        text: str,
    ):
        """Draw the text on the image overlay"""
        overlay.text(
            position, text, self.color, self.pil_font,
            anchor=getattr(self, 'anchor', None),
            align=getattr(self, 'align', 'left'),
            spacing=getattr(self, 'spacing', 0),
        )

    def set_multiline_properties(
        self,
        spacing: float,
        align: Literal['center', 'left', 'right'],
    ) -> 'Font':
        """Set rules for displaying multiline text"""
        self.align = align
        self.spacing = spacing

        return self


class Renderer:
    """Display fields on the image"""

    font: Font

    def __init__(self, font: Font) -> None:
        self.font = font

    def render(
        self,
        image: Image.Image,
        fields: Sequence[Field],
    ) -> Image.Image:
        """Draw the fields on the image"""
        copy = image.copy()
        overlay = ImageDraw.Draw(copy)
        self._draw_fields(overlay, fields)

        return copy

    def _draw_fields(
        self,
        overlay: ImageDraw.ImageDraw,
        fields: Sequence[Field],
    ) -> None:
        for field in fields:
            position = field.position.x, field.position.y
            self.font.draw(overlay, position, field.value)
