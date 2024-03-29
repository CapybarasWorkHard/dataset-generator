import argparse
import logging
import sys
import time
import traceback
import uuid
from pathlib import Path

from make_dataset import DocumentGenerator
from make_dataset.documents.rus_passport.page2 import generator as page2
from make_dataset.documents.rus_passport.page3 import generator as page3

DOCUMENTS = {
    'ru_passport_page2': page2,
    'ru_passport_page3': page3,
}


def enable_logging(level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        format='%(message)s',
        level=level,
    )


def get_uid() -> str:
    """Generate random uuid4"""
    uid = uuid.uuid4()
    name = str(uid).split('-')[:2]

    return ''.join(name)


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'document',
        action='store',
        choices=DOCUMENTS.keys(),
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

    return parser


def create_dataset(
    generator: DocumentGenerator,
    length: int,
    save_path: Path,
) -> None:
    for iteration in range(length):
        path = save_path / f'{get_uid()}.png'
        generator.generate().save(path)
        logging.info('[%i / %i] %s', iteration + 1, length, path)

    logging.info('Completed in %.3fs', time.process_time())


def main() -> None:
    try:
        parser = create_argument_parser()
        args = parser.parse_args()
        log_level = logging.CRITICAL if args.quiet else logging.DEBUG

        enable_logging(log_level)

        save_path = Path(args.dest)
        generator = DOCUMENTS.get(args.document)
        assert generator, 'No generator found'

        create_dataset(generator, args.dataset_length, save_path)
    except KeyboardInterrupt:
        logging.critical('Process stopped by user')
        sys.exit(0)
    except Exception as exc:
        logging.critical('Process stopped due to an uncaught exception')
        logging.error('%s: %s', type(exc), str(exc))
        logging.debug(traceback.format_exception(exc))
        sys.exit(1)


if __name__ == '__main__':
    main()
