import logging
import re
import time
from typing import Any, Literal, Self, TextIO
from dataclasses import dataclass

from .lang import _ # i18n function
from . import mapping
from ._json_parser import get_json_parser
from ._requests import read_url
from .constants import time_table

@dataclass
class Course:
    name: str
    weekday: Literal[1,2,3,4,5,6,7]
    room_name: str
    weeks: range
    update_date: tuple[int, int, int]
    periods: range
    class_name: str
    class_compose: list[str]
    teacher_name: str
    course_type: str
    exam_type: str
    credit: float
    zone: str
    form_code: str

    def __init__(self,
                 name: str,
                 weekday: str,
                 room_name: str,
                 weeks: str,
                 update_date: str,
                 periods: str,
                 teacher_name: str,
                 class_compose: str,
                 class_name: str,
                 course_type: str,
                 exam_type: str,
                 credit: str,
                 zone: str,
                 form_code: str):
        self.name = name
        self.weekday = self.parse_weekday(weekday)
        self.room_name = room_name
        self.weeks = self.parse_weeks(weeks)
        self.update_date = self.parse_date(update_date)
        self.periods = self.parse_periods(periods)
        self.teacher_name = teacher_name
        self.class_compose = self.parse_class(class_compose)
        self.class_name = class_name
        self.course_type = course_type
        self.exam_type = exam_type
        self.credit = float(credit)
        self.zone = zone
        self.form_code = form_code

    @staticmethod
    def parse_weekday(weekday: str) -> Literal[1,2,3,4,5,6,7]:
        match (iday := int(weekday)):
            case 1|2|3|4|5|6|7:
                return iday
            case _:
                raise ValueError(f"Invalid weekday: {weekday}")

    @staticmethod
    def parse_weeks(weeks: str) -> range:
        result = re.match(r"(\d+)-(\d+)周", weeks)
        if not result:
            raise ValueError(f"Invalid weeks: {weeks}")
        start, end = map(int, result.groups())
        return range(start, end + 1)

    @staticmethod
    def parse_periods(periods: str) -> range:
        result = re.match(r"(\d+)-(\d+)", periods)
        if not result:
            raise ValueError(f"Invalid periods: {periods}")
        start, end = map(int, result.groups())
        return range(start, end + 1)

    @staticmethod
    def parse_date(date: str) -> tuple[int, int, int]:
        time_tuple = time.strptime(date, "%Y-%m-%d")

        year = time_tuple.tm_year
        month = time_tuple.tm_mon
        day = time_tuple.tm_mday

        return (year, month, day)

    @staticmethod
    def parse_class(class_compose: str) -> list[str]:
        return class_compose.split(";")

    @property
    def description(self) -> str:
        return f"[{_(f'form.{self.form_code}.name')}{_(f'form.{self.form_code}.mark')}{self.exam_type}({self.credit})] {self.teacher_name}, {self.course_type}, {self.class_name}({','.join(self.class_compose)}), {self.zone}"

    @property
    def time(self) -> str:
        start_time = time_table[self.periods.start].split("-")[0]
        end_time = time_table[self.periods.stop-1].split("-")[1]
        return f"{start_time}-{end_time}"

    def __str__(self) -> str:
        return f"{self.name}:\n" \
               f"    {_('weekday')}: {self.weekday}\n" \
               f"    {_('periods')}: {self.periods.start}-{self.periods.stop-1}({self.time})\n" \
               f"    {_('weeks')}: {self.weeks.start}-{self.weeks.stop-1}{f'(/{self.weeks.step})' if self.weeks.step != 1 else ''}\n" \
               f"    {_('description')}: {self.description}\n\n"


class CourseTable:

    course_list: list[Course]

    def __init__(self):
        self.course_list = []

    @classmethod
    def from_json(cls, source: str) -> Self:
        self = cls()
        self.parse(get_json_parser().parse_str(source))
        return self

    @classmethod
    def from_file(cls, source: TextIO) -> Self:
        self = cls()
        self.parse(get_json_parser().parse_file(source))
        return self

    @classmethod
    def from_url(cls, source: str, **kwargs) -> Self:
        return cls.from_json(read_url(source, **kwargs))

    @classmethod
    def from_file_path(cls, path: str, encoding="utf-8") -> Self:
        with open(path, "r", encoding = encoding) as file:
            return cls.from_file(file)

    # def __setitem__(self, key: str, value: Any):
    #     if key in self.__annotations__:
    #         check_type(value, self.__annotations__[key])
    #         setattr(self, key, value)
    #     else:
    #         raise KeyError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    # def parse(self, data: dict):
    #     for key in self.__annotations__:
    #         ekey = mapping.find(key)
    #         match key:
    #             case "course_list":
    #                 self.parse_course_list(data.get(ekey, []))
    #                 break
    #             case _:
    #                 if ekey in data:
    #                     self[key] = data[ekey]
    #                 else:
    #                     self[key] = None


    def parse(self, data: dict):
        courses = data.get(mapping.find("course_list"), [])

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
                ikey = mapping.get(key)
                if ikey in course_args:
                    course_args[ikey] = course_raw[key]

            try:
                course_list.append(Course(**course_args))
            except Exception as e:
                logging.error(f"Failed to parse course {course_args}: {e}")

        self.course_list = course_list



    def pretty_print(self):
        pass
