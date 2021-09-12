import sys
from argparse import ArgumentParser, FileType

import dango
from .word import PartOfSpeech


def main():
    parser = ArgumentParser(description='Tokenize Japanese text')
    parser.add_argument('file', nargs='?', type=FileType('r'), default=sys.stdin,
                        help='a file containing text to be tokenized; if not specified standard input is read')

    args = parser.parse_args()

    try:
        for line in args.file:
            words = dango.tokenize(line.strip())
            surfaces = (w.surface for w in words if w.part_of_speech != PartOfSpeech.WHITESPACE)
            print(' '.join(surfaces), file=sys.stdout)
    except (BrokenPipeError, KeyboardInterrupt):
        sys.exit()


if __name__ == '__main__':
    main()
