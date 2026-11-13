"""Завантаження класів та учнів із CSV + створення співробітників."""

import csv
from pathlib import Path

from models import Director, Guard, School, SchoolClass, Student, Teacher

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_school(data_dir: Path = DATA_DIR) -> School:
    """Створити ОБ'ЄКТИ школи, класів, учнів і працівників із вихідних даних."""
    school = School("Демонстраційна школа")
    class_by_id: dict[str, SchoolClass] = {}

    # У classes.csv одна стрічка = один клас.
    with (data_dir / "classes.csv").open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file, delimiter=";"):
            class_id = row["class_id"].strip()
            school_class = SchoolClass(int(row["parallel"]), row["letter"])
            if class_id in class_by_id:
                raise ValueError(f"Повторний class_id: {class_id}")
            class_by_id[class_id] = school_class
            school.add_class(school_class)

    # У students.csv одна стрічка = один учень; class_id вказує його клас.
    with (data_dir / "students.csv").open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file, delimiter=";"):
            class_id = row["class_id"].strip()
            if class_id not in class_by_id:
                raise ValueError(f"У students.csv невідомий клас: {class_id}")
            raw_gender = row["gender"].strip().lower()
            if raw_gender in ("х", "хлопець", "ч"):
                gender = "Хлопець"
            elif raw_gender in ("д", "дівчина", "ж"):
                gender = "Дівчина"
            else:
                raise ValueError(f"Невідома стать: {row['gender']}")

            student = Student(
                surname=row["surname"].strip(),
                first_name=row["first_name"].strip(),
                patronymic=row["patronymic"].strip(),
                birth_year=int(row["birth_year"]),
                gender=gender,
                average_grade=float(row["average_grade"].replace(",", ".")),
            )
            class_by_id[class_id].add_student(student)

    # Працівників створюємо програмно, як цього вимагає сценарій 2.
    # Вони додаються до ТОГО САМОГО об'єкта School.
    school.add_employee(Director("Лисенко", "Олена", "Миколаївна", 15000, 24, 9))
    school.add_employee(Teacher("Мороз", "Ірина", "Павлівна", 12000, 21))
    school.add_employee(Teacher("Савчук", "Дмитро", "Ігорович", 12000, 16))
    school.add_employee(Teacher("Кириленко", "Оксана", "Вікторівна", 12000, 11))
    school.add_employee(Guard("Петренко", "Сергій", "Анатолійович", 11000, 15))
    return school
