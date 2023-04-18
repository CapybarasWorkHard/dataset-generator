import random
import textwrap

from faker import Faker
from PIL import Image

from documents.rus_passport import field_renderer, series_renderer
from make_dataset import DocumentGenerator
from make_dataset.factories.fields import FieldFactory
from make_dataset.positioning import Point
from make_dataset.render import FieldGroup


def get_random_department() -> str:
    department = random.choice(_department_names)
    text = department.format(
        city=faker.city(),
        district=random.choice(_district_names),
        region=faker.region(),
    )

    return textwrap.fill(text, 30).upper()


def get_random_department_code() -> str:
    first = random.randint(100, 999)
    second = random.randint(100, 999)

    return '{}-{}'.format(first, second)


_department_names = [
    'ТП №1 ОУФМС РОССИИ ПО {region} В {district} {city}',
    'ГУ МВД РОССИИ ПО {region}',
    'ОТДЕЛОМ УФМС РОССИИ ПО {region} В {city}',
    'ОТДЕЛОМ УФМС РОССИИ ПО {region} В {district} {city}',
    'ОТДЕЛЕНИЕМ УФМС РОССИИ ПО {region} В {district}',
    'ОТДЕЛЕНИЕМ УФМС РОССИИ ПО {region} В {city}',
    'ОТДЕЛОМ ВНУТРЕННИХ ДЕЛ {district} {region}',
    'ОТДЕЛОМ ВНУТРЕННИХ ДЕЛ {region}',
    'УПРАВЛЕНИЕМ ВНУТРЕННИХ ДЕЛ {city}'
]
_district_names = [
    'ДНЕПРОПЕТРОВСКОКАМЕНСКИЙ Р-Н',
    'ЖЕЛЕЗНОДОРОЖНЫЙ Р-Н',
    'КИРОВСКИЙ Р-Н',
    'КОНСТАНТИНОПОЛЬСКИЙ Р-Н',
    'РАЙОН ДОРОГОМИЛОВО',
    'РАЙОН СОКОЛЬНИКИ',
    'РАЙОН ЧЕРЁМУШКИ',
    'РАЙОН ЧЕРНОМЫРДИНСКИЙ САД',
    'ТУСОВОЧНЫЙ РАЙОН',
    'ЦАО',
]

faker = Faker('ru_RU')

fields = FieldGroup(field_renderer, (
    FieldFactory(
        'department',
        Point(780, 260),
        get_random_department,
        (38, 19),
    ),
    FieldFactory(
        'date_of_issue',
        Point(430, 500),
        lambda: faker.date(r'%d.%m.%Y'),
        (10, 7)
    ),
    FieldFactory(
        'department_code',
        Point(1100, 500),
        get_random_department_code,
        (10, 7),
    ),
))
series = FieldGroup(series_renderer, (
    FieldFactory(
        'series_first_part',
        Point(336, 83),
        lambda: str(random.randint(10, 99)),
    ),
    FieldFactory(
        'series_second_part',
        Point(458, 83),
        lambda: str(random.randint(10, 99)),
    ),
    FieldFactory(
        'number',
        Point(650, 83),
        lambda: str(random.randint(100000, 999999)),
    ),
))

image_source = 'images/passport-top.png'
image = Image.open(image_source)

passport_top_generator = DocumentGenerator(image, (fields, series))
