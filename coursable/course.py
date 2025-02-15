from datetime import datetime, timedelta
import re
import time
from typing import Literal
from dataclasses import dataclass

from .lang import _ # i18n function
from .constants import time_table, tz


@dataclass
class Course:
    name: str
    weekday: Literal[1,2,3,4,5,6,7]
    room_name: str
    weeks: range
    update_date: datetime
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
    def parse_date(date: str) -> datetime:
        time_tuple = time.strptime(date, "%Y-%m-%d")

        dt = datetime(time_tuple.tm_year,
                      time_tuple.tm_mon,
                      time_tuple.tm_mday,
                      tzinfo=tz)

        return dt

    @staticmethod
    def parse_class(class_compose: str) -> list[str]:
        return class_compose.split(";")

    @property
    def description(self) -> str:
        return f"[{_(f'form.{self.form_code}.name')}" \
               f"{_(f'form.{self.form_code}.mark')}" \
               f"{self.exam_type}({self.credit})]" \
               f"{self.teacher_name}, " \
               f"{self.course_type}, " \
               f"{self.class_name} " \
               f"({','.join(self.class_compose)}), " \
               f"{self.zone}"

    @property
    def time(self) -> tuple[timedelta, timedelta]:
        start_time = time_table[self.periods.start].split("-")[0].split(":")
        end_time = time_table[self.periods.stop-1].split("-")[1].split(":")
        st = timedelta(hours=int(start_time[0]), minutes=int(start_time[1]))
        et = timedelta(hours=int(end_time[0]), minutes=int(end_time[1]))
        return st, et

    def __str__(self) -> str:
        return f"{self.name}:\n" \
               f"    {_('weekday')}: {self.weekday}\n" \
               f"    {_('periods')}: {self.periods.start}-{self.periods.stop-1}({'-'.join(map(str, self.time))})\n" \
               f"    {_('room')}: {self.room_name}\n" \
               f"    {_('weeks')}: {self.weeks.start}-{self.weeks.stop-1}" \
                                 f"{f'(/{self.weeks.step})' if self.weeks.step != 1 else ''}\n" \
               f"    {_('description')}: {self.description}\n"
