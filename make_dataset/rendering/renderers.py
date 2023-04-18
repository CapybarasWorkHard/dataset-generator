from typing import Sequence

from PIL import ImageDraw
from PIL.Image import Image, Resampling, alpha_composite
from PIL.Image import new as new_image

from make_dataset.fields import Field
from make_dataset.rendering import Font, Renderer


class OpacityRenderer(Renderer):
    """Allows you to draw with translucent font"""

    def render(self, image: Image, fields: Sequence[Field]) -> Image:
        copy = image.convert('RGBA')
        text = new_image('RGBA', image.size, (0, 0, 0, 0))
        overlay = ImageDraw.Draw(text)
        self._draw_fields(overlay, fields)

        return alpha_composite(copy, text)


class RotationRenderer(Renderer):
    """Draw rotated text"""

    angle: float
    resampling: Resampling

    def __init__(self, font: Font, angle: float, resample: Resampling) -> None:
        super().__init__(font)
        self.angle = angle
        self.resampling = resample

    def render(self, image: Image, fields: Sequence[Field]) -> Image:
        copy = image.rotate(self.angle, self.resampling, True)
        overlay = ImageDraw.Draw(copy)
        self._draw_fields(overlay, fields)

        return copy.rotate(-self.angle, self.resampling, True)
