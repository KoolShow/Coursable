from urllib.parse import quote
from . import constants
import logging
from pathlib import Path
import traceback
from typing import TYPE_CHECKING, Self, TextIO

from .course import Course
from .mapping import to_external, to_internal
from .lang import _
from ._json_parser import parser
from ._lazy_imports import require


class CourseTable:

    course_list: list[Course]
    term: int

    def __init__(self):
        self.course_list = []
        self.term = -1

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
        requests = require("requests")
        text = requests.get(source, **kwargs, timeout=5).text

        return cls.from_json(text)

    @classmethod
    def from_file_path(cls, path: str | Path, encoding="utf-8") -> Self:
        with open(path, "r", encoding = encoding) as file:
            return cls.from_file(file)

    def parse(self, data: dict):
        courses = data.get(to_external("course_list"), [])
        student = data.get(to_external("student"), {})
        term = student.get(to_external("term"), '')
        if term:
            self.term = int(term)

        if not courses:
            raise ValueError("Course list not found or is empty")

        course_list = []
        for course_raw in courses:
            course_args = {
                'name': '',
                'weekday': '',
                'room_name': '',
                'year': '',
                'term': '',
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

            if len(course_args['year']) > 4:
                course_args['year'] = course_args['year'][:4]
            if not course_args['term']:
                course_args['term'] = str(self.term)

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

    def to_ics(self, filename: str):
        Calendar = require("icalendar").Calendar # pylint: disable=C0103
        if TYPE_CHECKING: from icalendar import Calendar # pylint: disable=C0321,C0415

        cal = Calendar()

        cal.add('prodid', constants.PROD_ID)
        cal.add('version', '2.0')
        for course in self.course_list:
            event = course.to_event()
            cal.add_component(event)

        with open(filename, 'wb') as f:
            f.write(cal.to_ical())
