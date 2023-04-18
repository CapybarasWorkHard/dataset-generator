from make_dataset.fields import Field
from make_dataset.render import Font


def get_field_text_position(font: Font, field: Field) -> tuple[int, ...]:
    center = tuple(field.point)
    bbox = font.pil_font.getbbox(field.value, anchor=font.anchor)

    return tuple(
        a + b
        for a, b in zip(center * 2, bbox)
    )
