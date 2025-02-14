import argparse
from pathlib import Path

from .utils import absolute_path
from . import CourseTable


def main():
    parser = argparse.ArgumentParser(
        description="BJUT course table converter."
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1',
        help="Show the version of the tool."
    )

    parser.add_argument(
        '-i', '--input',
        metavar='INPUT_FILE',
        type=str,
        help="The path to the input file. If not provided, the input will be the default example."
    )

    args = parser.parse_args()

    input_file: str | Path = args.input or absolute_path("examples/example.json")

    try:
        table = CourseTable.from_file_path(input_file)
    except FileNotFoundError as e:
        parser.error(str(e))

    for course in table.course_list:
        print(course)

if __name__ == "__main__":
    main()
