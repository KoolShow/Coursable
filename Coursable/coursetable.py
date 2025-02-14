import logging
from pathlib import Path
import traceback
from typing import Self, TextIO

from .course import Course
from .mapping import to_external, to_internal
from .lang import _
from ._json_parser import parser
from ._requests import read_url


class CourseTable:

    course_list: list[Course]

    def __init__(self):
        self.course_list = []

    @classmethod
    def from_json(cls, source: str) -> Self:
        self = cls()
        self.parse(parser.parse_str(source))
        return self

    @classmethod
    def from_file(cls, source: TextIO) -> Self:
        self = cls()
        self.parse(parser.parse_file(source))
        return self

    @classmethod
    def from_url(cls, source: str, **kwargs) -> Self:
        return cls.from_json(read_url(source, **kwargs))

    @classmethod
    def from_file_path(cls, path: str | Path, encoding="utf-8") -> Self:
        with open(path, "r", encoding = encoding) as file:
            return cls.from_file(file)

    def parse(self, data: dict):
        courses = data.get(to_external("course_list"), [])

        if not courses:
            raise ValueError("Course list not found or is empty")

        course_list = []
        for course_raw in courses:
            course_args = {
                'name': '',
                'weekday': '',
                'room_name': '',
                'weeks': '',
                'update_date': '',
                'periods': '',
                'teacher_name': '',
                'class_compose': '',
                'class_name': '',
                'course_type': '',
                'exam_type': '',
                'credit': '',
                'zone': '',
                'form_code': ''
            }

            for key in course_raw:
                ikey = to_internal(key)
                if ikey in course_args:
                    course_args[ikey] = course_raw[key]

            try:
                course_list.append(Course(**course_args))
            except Exception:
                logging.error("Unexpected error occurred while parsing course %s, %s",
                              course_args, traceback.format_exc())

        self.course_list = course_list



    def __str__(self) -> str:
        return f"{_('coursetable')}:\n    " \
               +"\n".join(str(course) for course in self.course_list) \
                .replace("\n", "\n    ") \
                .strip(" ")
