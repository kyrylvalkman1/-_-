"""Невеликі автоматичні перевірки проєкту: python -m unittest discover -s tests."""

import tempfile
import unittest
from pathlib import Path

from data_loader import load_school
from models import Director, Guard, Teacher
from salary_cli import export_salaries


class SchoolProjectTests(unittest.TestCase):
    def test_csv_and_initial_statistics(self) -> None:
        school = load_school()
        self.assertEqual(len(school.classes), 22)
        self.assertGreater(school.statistics().total_students, 0)
        self.assertAlmostEqual(
            school.statistics().boys_percent + school.statistics().girls_percent, 100
        )
        self.assertEqual(len(school.employees), 5)

    def test_promotion_preserves_students_and_removes_graduates(self) -> None:
        school = load_school()
        all_before = school.statistics().total_students
        survivors = {
            id(school_class): tuple(school_class.students)
            for school_class in school.classes if school_class.parallel < 11
        }
        removed = sum(item.student_count for item in school.classes if item.parallel == 11)
        graduates = school.promote_one_year()
        self.assertEqual(graduates, removed)
        self.assertEqual(school.statistics().total_students, all_before - removed)
        self.assertEqual(len(school.classes), 20)
        self.assertEqual({item.parallel for item in school.classes}, set(range(2, 12)))
        for school_class in school.classes:
            self.assertEqual(school_class.students, survivors[id(school_class)])

    def test_salary_formulas(self) -> None:
        school = load_school()
        director = next(item for item in school.employees if isinstance(item, Director))
        teacher = next(item for item in school.employees if isinstance(item, Teacher))
        guard = next(item for item in school.employees if isinstance(item, Guard))
        self.assertEqual(director.calculate_salary(), 11700)
        self.assertEqual(teacher.calculate_salary(), 8400)
        self.assertEqual(guard.calculate_salary(), 14750)

    def test_csv_export(self) -> None:
        school = load_school()
        with tempfile.TemporaryDirectory() as temporary_dir:
            file = Path(temporary_dir) / "salary.csv"
            export_salaries(school, file)
            self.assertTrue(file.exists())
            self.assertEqual(len(file.read_text(encoding="utf-8-sig").splitlines()), 6)


if __name__ == "__main__":
    unittest.main()
