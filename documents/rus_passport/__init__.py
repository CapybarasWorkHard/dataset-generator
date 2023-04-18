from pathlib import Path

from PIL.Image import Resampling

from make_dataset.render import Font
from make_dataset.render.renderers import OpacityRenderer, RotationRenderer

root_dir = Path(__file__).resolve().parent.parent.parent
fonts_dir = root_dir / 'fonts'
images_dir = root_dir / 'images'

series_font = Font('#660c0c', fonts_dir / 'upcel.ttf', 84, 'ms')
field_font = Font(
    (0, 0, 0, 165),
    fonts_dir / 'cambriab.ttf',
    48,
    'ms',
    32,
    'center',
)

field_renderer = OpacityRenderer(field_font)
series_renderer = RotationRenderer(series_font, 90, Resampling.BICUBIC)
