import random
from pathlib import Path
from typing import Generic, Literal, Sequence, TypeAlias, TypeVar

from PIL import Image, ImageDraw, ImageFont

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

    def __init__(self, image: Image.Image, groups: Sequence['FieldGroup']) -> None:
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

    def __repr__(self) -> str:
        return f'{self.name}: \'{self.value}\' at {self.position}'


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

    font: Font

    def __init__(self, font: Font) -> None:
        self.font = font

    def render(self, image: Image.Image, fields: Sequence[Field]) -> Image.Image:
        """Draw the fields on the image"""
        copy = image.copy()
        overlay = ImageDraw.Draw(copy)
        self._draw_fields(overlay, fields)

        return copy

    def _draw_fields(self, overlay: ImageDraw.ImageDraw, fields: Sequence[Field]) -> None:
        for field in fields:
            position = field.position.x, field.position.y
            self.font.draw(overlay, position, field.value)


class Position:
    """Position of anything on the image with pixels"""

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __iter__(self):
        for attr in self.x, self.y:
            yield attr

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.x}, {self.y})'

    def shift(self, vertical: int, horizontal: int) -> 'Position':
        """Get new shifted position"""
        return Position(self.x + horizontal, self.y + vertical)


class Offset:
    """Offset from the position in pixels"""

    vertical: float
    horizontal: float

    @classmethod
    def random(cls, x_limit: int, y_limit: int):
        assert x_limit > 0 and y_limit > 0
        horizontal = random.randint(-x_limit, x_limit)
        vertical = random.randint(-y_limit, y_limit)

        return cls(vertical, horizontal)

    def __init__(self, vertical: float, horizontal: float) -> None:
        self.vertical = vertical
        self.horizontal = horizontal

    def __iter__(self):
        for attr in self.vertical, self.horizontal:
            yield attr

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.vertical}, {self.horizontal}'

    def apply(self, x: int, y: int) -> tuple[float, float]:
        """Add the offset to a position"""
        return x + self.horizontal, y + self.vertical
