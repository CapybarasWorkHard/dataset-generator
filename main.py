import argparse
import time
import uuid
from pathlib import Path

from documents.passport_bottom import passport_bottom_generator
from documents.passport_top import passport_top_generator

documents = {
    'passport_bottom': passport_bottom_generator,
    'passport_top': passport_top_generator,
}


def get_uid() -> str:
    """Generate random uuid4 """
    uid = uuid.uuid4()
    return str(uid).replace('-', '')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'document',
        action='store',
        choices=documents.keys(),
    )
    parser.add_argument(
        'dest',
        action='store',
        help='директория, в которую будут сохранятся сгенерированные файлы',
    )
    parser.add_argument(
        '-l', '--dataset-length',
        action='store',
        type=int,
        default=500,
        help='количество сгенерированных файлов',
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='не выводить ничего в консоль'
    )
    args = parser.parse_args()

    save_path = Path(args.dest).resolve()
    generator = documents.get(args.document)
    assert generator, 'No generator found'

    for iteration in range(args.dataset_length):
        new_name = save_path / f'{get_uid()}.png'
        generator.generate().save(new_name)

        if args.quiet:
            continue

        print(f'[{iteration + 1} / {args.dataset_length}] {new_name}')

    if not args.quiet:
        print('\n', f'completed in {time.process_time():.3f}s')
