from datetime import datetime
import unittest
from coursable import Course
from coursable.constants import tz

class TestCourse(unittest.TestCase):

    def test_parse_weekday(self):
        self.assertEqual(Course.parse_weekday('1'), 1)
        with self.assertRaises(ValueError):
            Course.parse_weekday('8')

    def test_parse_weeks(self):
        self.assertEqual(Course.parse_weeks('1-16周'), range(1, 17))
        with self.assertRaises(ValueError):
            Course.parse_weeks('invalid')

    def test_parse_periods(self):
        self.assertEqual(Course.parse_periods('1-4'), range(1, 5))
        with self.assertRaises(ValueError):
            Course.parse_periods('invalid')

    def test_parse_date(self):
        self.assertEqual(Course.parse_date('2023-02-14'), datetime(2023, 2, 14, tzinfo=tz))
        with self.assertRaises(ValueError):
            Course.parse_date('invalid')

    def test_parse_class(self):
        self.assertEqual(Course.parse_class('class1;class2'), ['class1', 'class2'])

    def test_course_initialization(self):
        course = Course(
            name="Test Course",
            weekday="1",
            room_name="Room 101",
            weeks="1-16周",
            update_date="2023-02-14",
            periods="1-4",
            teacher_name="Teacher A",
            class_compose="class1;class2",
            class_name="Class A",
            course_type="Type A",
            exam_type="Exam A",
            credit="3.0",
            zone="Zone A",
            form_code="Code A"
        )
        self.assertEqual(course.name, "Test Course")
        self.assertEqual(course.weekday, 1)
        self.assertEqual(course.room_name, "Room 101")
        self.assertEqual(course.weeks, range(1, 17))
        self.assertEqual(course.update_date, datetime(2023, 2, 14, tzinfo=tz))
        self.assertEqual(course.periods, range(1, 5))
        self.assertEqual(course.teacher_name, "Teacher A")
        self.assertEqual(course.class_compose, ["class1", "class2"])
        self.assertEqual(course.class_name, "Class A")
        self.assertEqual(course.course_type, "Type A")
        self.assertEqual(course.exam_type, "Exam A")
        self.assertEqual(course.credit, 3.0)
        self.assertEqual(course.zone, "Zone A")
        self.assertEqual(course.form_code, "Code A")

if __name__ == '__main__':
    unittest.main()