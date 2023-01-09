# Dataset generator

Генератор документов позволяет создавать датасеты из документов с данными для обучения нейронных сетей.

## Использование

### В консоли

    python main.py {document} {dest} -l {count}

### Из кода

**Пример 1**. Вставка неизменяемых данных на изображение

```python
from PIL import Image
from models import DocumentGenerator, FieldGroup, Font, Renderer, Field, Position

surname = Field('name', Position(100, 100), 'Иванов')
first_name = Field('name', Position(100, 100), 'Иван')
middle_name = Field('name', Position(100, 100), 'Иванович')

font = Font('#000', 'font.ttf', 32)
renderer = Renderer(font)
full_name = FieldGroup(renderer, (surname, first_name, middle_name))

image = Image.open('template.png')
generator = DocumentGenerator(image, [full_name])
```

**Пример 2**. Использование FieldFactory для геренации данных

```python
from faker import Faker
from PIL import Image
from factories import FieldFactory
from models import DocumentGenerator, FieldGroup, Font, Position, Renderer


def generate_surname() -> str:
    ...


faker = Faker('ru_RU')

surname = FieldFactory('name', Position(100, 100), generate_surname)
first_name = FieldFactory('name', Position(100, 100), faker.first_name)
middle_name = FieldFactory(
    'name', Position(100, 100),
    value_function=lambda: 'Постоянное имя',
)

font = Font('#000', 'font.ttf', 32)
renderer = Renderer(font)
full_name = FieldGroup(renderer, (surname, first_name, middle_name))

image = Image.open('template.png')
generator = DocumentGenerator(image, [full_name])
```
