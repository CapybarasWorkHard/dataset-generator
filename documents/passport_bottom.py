import random

from faker import Faker
from PIL import Image
from PIL.Image import Resampling

from make_dataset import DocumentGenerator
from make_dataset.factories.fields import FieldFactory
from make_dataset.fields import FieldGroup
from make_dataset.positioning import Point
from make_dataset.rendering import Font, renderers

faker = Faker('ru_RU')

last_name = FieldFactory(
    'last_name', Point(937, 218),
    value_function=lambda: faker.last_name().upper(),
    offset_limit=(20, 10),
)
first_name = FieldFactory(
    'first_name', Point(937, 370),
    value_function=lambda: faker.first_name().upper(),
    offset_limit=(20, 10),
)
middle_name = FieldFactory(
    'middle_name', Point(937, 440),
    value_function=lambda: faker.middle_name().upper(),
    offset_limit=(20, 10),
)
sex = FieldFactory(
    'sex', Point(630, 510),
    value_function=lambda: random.choice(['МУЖ.', 'ЖЕН.']),
    offset_limit=(20, 10),
)
birth_date = FieldFactory(
    'birth_date', Point(1055, 510),
    value_function=lambda: faker.date_of_birth(
        minimum_age=14,
        maximum_age=60,
    ).strftime(r'%d.%m.%Y'),
    offset_limit=(20, 10),
)
birth_place = FieldFactory(
    'birth_place', Point(937, 580),
    value_function=lambda: faker.city().upper(),
    offset_limit=(20, 10),
)
series_first_part = FieldFactory(
    'series_first_part', Point(336, 1488 - 1405),
    value_function=lambda: str(random.randint(10, 99)),
)
series_second_part = FieldFactory(
    'series_second_part', Point(458, 1488 - 1405),
    value_function=lambda: str(random.randint(10, 99)),
)
number = FieldFactory(
    'number', Point(650, 1488 - 1405),
    value_function=lambda: str(random.randint(100000, 999999)),
)

field_font = Font((0, 0, 0, 165), 'fonts/cambriab.ttf', 48, 'ms')
field_renderer = renderers.OpacityRenderer(field_font)
fields = FieldGroup(field_renderer, (
    last_name,
    first_name,
    middle_name,
    sex,
    birth_date,
    birth_place,
))

series_font = Font('#660c0c', 'fonts/upcel.ttf', 84, 'ms')
series_renderer = renderers.RotationRenderer(
    series_font, 90, Resampling.BICUBIC
)
series = FieldGroup(series_renderer, (
    series_first_part,
    series_second_part,
    number
))

image_source = 'images/passport-bottom.png'
image = Image.open(image_source)

passport_bottom_generator = DocumentGenerator(image, (fields, series))
