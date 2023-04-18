from pathlib import Path
from typing import Literal, Sequence, TypeAlias

from PIL import Image, ImageDraw, ImageFont

from make_dataset.fields import Field

_Color: TypeAlias = int | str | tuple[int, ...]


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
            position = field.point.x, field.point.y
            self.font.draw(overlay, position, field.value)
