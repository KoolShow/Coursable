import argparse
from pathlib import Path

from .utils import absolute_path
from . import CourseTable
from . import __version__


def main():
    parser = argparse.ArgumentParser(
        prog = __package__,
        description = "BJUT course table converter."
    )

    parser.add_argument(
        '-v', '--version',
        action = 'version',
        version = f'%(prog)s {__version__}',
        help="Show the version of the tool."
    )

    parser.add_argument(
        '-i', '--input',
        metavar = 'INPUT_FILE',
        type = str,
        help = "The path to the input file. If not provided, the input will be the default example."
    )

    parser.add_argument(
        '-c', '--ics',
        metavar = 'OUTPUT_ICS_FILE',
        type = str,
        help = "Set output format to ics, and specify the output file path."
    )

    args = parser.parse_args()

    input_file: str | Path = args.input or absolute_path("examples/example.json")

    try:
        table = CourseTable.from_file_path(input_file)
    except FileNotFoundError as e:
        parser.error(str(e))

    if args.ics:
        table.to_ics(args.ics)
    else:
        print(table)

if __name__ == "__main__":
    main()
