from PIL import Image, ImageDraw

from models import Factory, Field, Font, Renderer


class OpacityRenderer(Renderer):
    """Allows you to draw with translucent font"""

    def render(self, image: Image.Image) -> Image.Image:
        copy = image.convert('RGBA')
        text = Image.new('RGBA', image.size, (0, 0, 0, 0))
        overlay = ImageDraw.Draw(text)
        self._draw_fields(overlay)

        return Image.alpha_composite(copy, text)


class RotationRenderer(Renderer):
    """Draw rotated text"""

    angle: float
    resampling: Image.Resampling

    def __init__(
        self,
        font: Font,
        angle: float,
        resampling: Image.Resampling,
        *fields: Field | Factory[Field],
    ) -> None:
        super().__init__(font, *fields)
        self.angle = angle
        self.resampling = resampling

    def render(self, image: Image.Image) -> Image.Image:
        copy = image.rotate(self.angle, self.resampling, True)
        overlay = ImageDraw.Draw(copy)
        self._draw_fields(overlay)

        return copy.rotate(-self.angle, self.resampling, True)
