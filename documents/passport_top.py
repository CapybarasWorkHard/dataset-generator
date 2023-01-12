import random
from textwrap import fill

from faker import Faker
from PIL.Image import open

from datasetgenerator.factories import FieldFactory
from datasetgenerator.models import DocumentGenerator, FieldGroup, Position
from datasetgenerator.models.renderers import OpacityRenderer
from documents.passport_bottom import field_font, series_renderer

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

department = FieldFactory(
    'department', Position(780, 260),
    value_function=lambda: fill(width=30, text=random.choice(
        _department_names).format(
            city=faker.city(),
            district=random.choice(_district_names),
            region=faker.region(),
    ).upper()),
    offset_limit=(38, 19),
)
date_of_issue = FieldFactory(
    'date_of_issue', Position(430, 500),
    value_function=lambda: faker.date(r'%d.%m.%Y'),
    offset_limit=(10, 7)
)
department_code = FieldFactory(
    'department_code', Position(1100, 500),
    value_function=lambda: '{}-{}'.format(
        random.randint(100, 999),
        random.randint(100, 999),
    ),
    offset_limit=(10, 7),
)
series_first_part = FieldFactory(
    'series_first_part', Position(336, 83),
    value_function=lambda: str(random.randint(10, 99)),
)
series_second_part = FieldFactory(
    'series_second_part', Position(458, 83),
    value_function=lambda: str(random.randint(10, 99)),
)
number = FieldFactory(
    'number', Position(650, 83),
    value_function=lambda: str(random.randint(100000, 999999)),
)

field_font.set_multiline_properties(32, 'center')

fields = FieldGroup(OpacityRenderer(field_font), (
    department,
    date_of_issue,
    department_code,
))
series = FieldGroup(series_renderer, (
    series_first_part,
    series_second_part,
    number,
))

passport_top_generator = DocumentGenerator(
    open('images/passport-top.png'),
    (fields, series),
)
