from make_dataset.fields import Field
from make_dataset.render import Font


def get_field_text_position(font: Font, field: Field) -> tuple[int, ...]:
    center = tuple(field.point)
    bbox = font.pil_font.getbbox(field.value, anchor=font.anchor)

    return tuple(
        a + b
        for a, b in zip(center * 2, bbox)
    )


def get_field_multiline_text_position(
    font: Font,
    field: Field,
) -> list[tuple[int, ...]]:
    positions: list[tuple[int, ...]] = []

    for index, line in enumerate(field.value.splitlines()):
        bbox = font.pil_font.getbbox(line, anchor=font.anchor)
        offset = int(index * (font.size + font.spacing))
        new_center = tuple(field.point.shift(0, offset))
        text_pos = tuple(
            a + b
            for a, b in zip(new_center * 2, bbox)
        )
        positions.append(text_pos)

    return positions
