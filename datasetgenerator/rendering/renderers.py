from typing import Sequence

from PIL import Image, ImageDraw
from PIL.Image import Resampling

from datasetgenerator.models import Field, Renderer
from datasetgenerator.rendering import Font


class OpacityRenderer(Renderer):
    """Allows you to draw with translucent font"""

    def render(self, image: Image.Image, fields: Sequence[Field]) -> Image.Image:
        copy = image.convert('RGBA')
        text = Image.new('RGBA', image.size, (0, 0, 0, 0))
        overlay = ImageDraw.Draw(text)
        self._draw_fields(overlay, fields)

        return Image.alpha_composite(copy, text)


class RotationRenderer(Renderer):
    """Draw rotated text"""

    angle: float
    resampling: Resampling

    def __init__(self, font: Font, angle: float, resampling: Resampling) -> None:
        super().__init__(font)
        self.angle = angle
        self.resampling = resampling

    def render(self, image: Image.Image, fields: Sequence[Field]) -> Image.Image:
        copy = image.rotate(self.angle, self.resampling, True)
        overlay = ImageDraw.Draw(copy)
        self._draw_fields(overlay, fields)

        return copy.rotate(-self.angle, self.resampling, True)
