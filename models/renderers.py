from PIL import Image, ImageDraw

from models import Renderer


class OpacityRenderer(Renderer):
    """Allows you to draw with translucent font"""

    def render(self, image: Image.Image) -> Image.Image:
        copy = image.convert('RGBA')
        text = Image.new('RGBA', image.size, (0, 0, 0, 0))
        overlay = ImageDraw.Draw(text)
        self._draw_fields(overlay)

        return Image.alpha_composite(copy, text)
