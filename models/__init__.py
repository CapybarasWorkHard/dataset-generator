import random
from pathlib import Path
from typing import Generator, Generic, Literal, Sequence, TypeAlias, TypeVar

from PIL import Image, ImageDraw, ImageFont

_Color: TypeAlias = int | str | tuple[int, ...]
_InstanceType = TypeVar('_InstanceType')


class DocumentGenerator:
    """Render all fields on an image using renderers"""

    image: Image.Image
    renderers: Sequence['Renderer']

    def __init__(self, image: Image.Image, renderers: Sequence['Renderer']) -> None:
        self.image = image
        self.renderers = renderers

    def generate(self) -> Image.Image:
        """Walk throught the renderers and draw fields to the image"""
        image = self.image

        for renderer in self.renderers:
            image = renderer.render(image)

        return image


class Factory(Generic[_InstanceType]):
    """Allows you to dynamically create classes"""

    def create(self) -> _InstanceType:
        raise NotImplementedError()


class Field:
    """Editable document field"""

    name: str
    position: 'Position'
    value: str

    def __init__(
        self,
        name: str,
        position: 'Position',
        value: str,
    ) -> None:
        self.name = name
        self.position = position
        self.value = value


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

    def draw(self, overlay: ImageDraw.ImageDraw, position: tuple[float, float], text: str):
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

    fields: Sequence[Field]
    font: Font

    def __init__(self, font: Font, fields: Sequence[Field | Factory[Field]]) -> None:
        self.fields = tuple(self._seed_fields(fields))
        self.font = font

    def render(self, image: Image.Image) -> Image.Image:
        """Draw the fields on the image"""
        copy = image.copy()
        overlay = ImageDraw.Draw(copy)
        self._draw_fields(overlay)

        return copy

    def _draw_fields(self, overlay: ImageDraw.ImageDraw) -> None:
        for field in self.fields:
            position = field.position.x, field.position.y
            self.font.draw(overlay, position, field.value)

    def _seed_fields(self, sequence: Sequence[Field | Factory[Field]]) -> Generator[Field, None, None]:
        for item in sequence:
            match  item:
                case Factory():
                    yield item.create()
                case Field():
                    yield item
                case _:
                    raise TypeError(type(item), (Field, Factory[Field]))


class Position:
    """Position of anything on the image with pixels"""

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def shift(self, vertical: int, horizontal: int) -> 'Position':
        """Get new shifted position"""
        return Position(self.x + horizontal, self.y + vertical)


class Offset:
    """Offset from the position in pixels"""

    vertical: float
    horizontal: float

    def __init__(self, vertical: float, horizontal: float) -> None:
        self.vertical = vertical
        self.horizontal = horizontal

    @classmethod
    def random(cls, x_limit: int, y_limit: int):
        assert x_limit > 0 and y_limit > 0
        vertical = random.randint(-x_limit, x_limit)
        horizontal = random.randint(-y_limit, y_limit)

        return cls(vertical, horizontal)

    def apply(self, x: int, y: int) -> tuple[float, float]:
        """Add the offset to a position"""
        return x + self.horizontal, y + self.vertical
