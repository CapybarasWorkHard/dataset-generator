# Dataset generator

Генератор документов позволяет создавать документы с данными для обучения нейронных сетей.

## Использование

### В консоли

    python -m make_dataset {document} {dest} -l {count}

Где:

- **document** – название генератора
- **dest** – директория, в которую будут сохраняться документы
- **count** – количество файлов для генерации

### Из кода

**Пример 1**. Вставка неизменяемых данных на изображение

```python
from PIL import Image

from make_dataset import DocumentGenerator, FieldGroup
from make_dataset.fields import Field
from make_dataset.positioning import Point
from make_dataset.render import Font, Renderer

surname = Field('name', Point(100, 100), 'Иванов')
first_name = Field('name', Point(100, 100), 'Иван')
middle_name = Field('name', Point(100, 100), 'Иванович')

font = Font('#000', 'font.ttf', 32)
renderer = Renderer(font)
full_name = FieldGroup(renderer, (
    surname,
    first_name,
    middle_name,
))

image = Image.open('template.png')
generator = DocumentGenerator(image, [full_name])

generator.generate().show()
```

**Пример 2**. Использование `FieldFactory` для генерации данных

```python
from faker import Faker
from PIL import Image

from make_dataset import DocumentGenerator, FieldGroup
from make_dataset.factories.fields import FieldFactory
from make_dataset.positioning import Point
from make_dataset.render import Font, Renderer


faker = Faker('ru_RU')

name = FieldFactory('name', Point(100, 100), faker.first_name)
surname = FieldFactory(
    'surname',
    Point(100, 100),
    lambda: 'Постоянное имя',
)

font = Font('#000', 'font.ttf', 32)
renderer = Renderer(font)
full_name = FieldGroup(renderer, (name, surname))

image = Image.open('template.png')
generator = DocumentGenerator(image, [full_name])

generator.generate().show()
```
