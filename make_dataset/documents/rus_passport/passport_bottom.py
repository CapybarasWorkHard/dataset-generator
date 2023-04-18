import random

from faker import Faker
from PIL import Image

from make_dataset.documents.rus_passport import (
    field_renderer,
    images_dir,
    series_renderer
)
from make_dataset import DocumentGenerator
from make_dataset.factories.fields import FieldFactory
from make_dataset.positioning import Point
from make_dataset.render import FieldGroup

faker = Faker('ru_RU')

fields = FieldGroup(field_renderer, (
    FieldFactory(
        'last_name',
        Point(937, 218),
        lambda: faker.last_name().upper(),
        (20, 10),
    ),
    FieldFactory(
        'first_name',
        Point(937, 370),
        lambda: faker.first_name().upper(),
        (20, 10),
    ),
    FieldFactory(
        'middle_name',
        Point(937, 440),
        lambda: faker.middle_name().upper(),
        (20, 10),
    ),
    FieldFactory(
        'sex',
        Point(630, 510),
        lambda: random.choice(['МУЖ.', 'ЖЕН.']),
        (20, 10),
    ),
    FieldFactory(
        'birth_date',
        Point(1055, 510),
        lambda: faker.date_of_birth(
            minimum_age=14,
            maximum_age=60,
        ).strftime(r'%d.%m.%Y'),
        (20, 10),
    ),
    FieldFactory(
        'birth_place',
        Point(937, 580),
        lambda: faker.city().upper(),
        (20, 10),
    ),
))
series = FieldGroup(series_renderer, (
    FieldFactory(
        'series_first_part',
        Point(336, 1488 - 1405),
        lambda: str(random.randint(10, 99)),
    ),
    FieldFactory(
        'series_second_part',
        Point(458, 1488 - 1405),
        lambda: str(random.randint(10, 99)),
    ),
    FieldFactory(
        'number',
        Point(650, 1488 - 1405),
        lambda: str(random.randint(100000, 999999)),
    ),
))

image_source = images_dir / 'passport-bottom.png'
image = Image.open(image_source)

passport_bottom_generator = DocumentGenerator(image, (fields, series))
