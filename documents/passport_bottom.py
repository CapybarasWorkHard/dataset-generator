import random

from faker import Faker
from PIL.Image import Resampling, open

from factories import FieldFactory
from models import DocumentGenerator, FieldGroup, Font, Position
from models.renderers import OpacityRenderer, RotationRenderer

faker = Faker('ru_RU')

last_name = FieldFactory(
    'last_name', Position(937, 218),
    value_function=lambda: faker.last_name().upper(),
)
first_name = FieldFactory(
    'first_name', Position(937, 370),
    value_function=lambda: faker.first_name().upper(),
)
middle_name = FieldFactory(
    'middle_name', Position(937, 440),
    value_function=lambda: faker.middle_name().upper(),
)
sex = FieldFactory(
    'sex', Position(630, 510),
    value_function=lambda: random.choice(['МУЖ.', 'ЖЕН.']),
)
birth_date = FieldFactory(
    'birth_date', Position(1055, 510),
    value_function=lambda: faker.date_of_birth(
        minimum_age=14,
        maximum_age=60,
    ).strftime(r'%d.%m.%Y'),
)
birth_place = FieldFactory(
    'birth_place', Position(937, 580),
    value_function=lambda: faker.city().upper(),
)
series_first_part = FieldFactory(
    'series_first_part', Position(336, 1488 - 1405),
    value_function=lambda: str(random.randint(10, 99)),
)
series_second_part = FieldFactory(
    'series_second_part', Position(458, 1488 - 1405),
    value_function=lambda: str(random.randint(10, 99)),
)
number = FieldFactory(
    'number', Position(650, 1488 - 1405),
    value_function=lambda: str(random.randint(100000, 999999)),
)

field_font = Font((0, 0, 0, 165), 'fonts/cambriab.ttf', 48, 'ms')
field_renderer = OpacityRenderer(field_font)

series_font = Font('#660c0c', 'fonts/upcel.ttf', 84, 'ms')
series_renderer = RotationRenderer(series_font, 90, Resampling.BICUBIC)

fields = FieldGroup(field_renderer, (
    last_name,
    first_name,
    middle_name,
    sex,
    birth_date,
    birth_place,
))
series = FieldGroup(series_renderer, (
    series_first_part,
    series_second_part,
    number
))

passport_bottom_generator = DocumentGenerator(
    open('images/passport-bottom.png'),
    (fields, series),
)
