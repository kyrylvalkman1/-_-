"""Спільні моделі школи для обох сценаріїв (Python 3.11+)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Iterator, Literal

Gender = Literal["Хлопець", "Дівчина"]


@dataclass(frozen=True, slots=True)
class Student:
    """Учень із персональними даними та середньою оцінкою."""

    surname: str
    first_name: str
    patronymic: str
    birth_year: int
    gender: Gender
    average_grade: float

    def __post_init__(self) -> None:
        # Перевірка даних під час створення об'єкта.
        if not 1 <= self.average_grade <= 12:
            raise ValueError("Середня оцінка має бути від 1 до 12.")
        if not 1900 <= self.birth_year <= 2100:
            raise ValueError("Некоректний рік народження.")

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.first_name} {self.patronymic}"


@dataclass(slots=True)
class SchoolClass:
    """Клас: паралель, літера та учні, які до нього належать."""

    parallel: int
    letter: str
    _students: list[Student] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if not 1 <= self.parallel <= 11:
            raise ValueError("Паралель повинна бути від 1 до 11.")
        if not self.letter.strip():
            raise ValueError("Вертикаль (літера) не може бути порожньою.")
        self.letter = self.letter.strip().upper()

    @property
    def name(self) -> str:
        return f"{self.parallel}-{self.letter}"

    @property
    def students(self) -> tuple[Student, ...]:
        # Повертаємо незмінюваний набір посилань на учнів.
        return tuple(self._students)

    @property
    def student_count(self) -> int:
        return len(self._students)

    def add_student(self, student: Student) -> None:
        self._students.append(student)

    def promote(self) -> None:
        """Перевести клас на одну паралель вище, не змінюючи учнів."""
        if self.parallel == 11:
            raise ValueError("11-й клас випускається, а не переходить у 12-й.")
        self.parallel += 1


class Employee(ABC):
    """Абстрактний базовий клас працівника (наслідування й поліморфізм)."""

    position: ClassVar[str] = "Працівник"

    def __init__(
        self,
        surname: str,
        first_name: str,
        patronymic: str,
        base_salary: float,
    ) -> None:
        if base_salary < 0:
            raise ValueError("Ставка не може бути від'ємною.")
        self.surname = surname
        self.first_name = first_name
        self.patronymic = patronymic
        self.base_salary = float(base_salary)

    @property
    def full_name(self) -> str:
        return f"{self.surname} {self.first_name} {self.patronymic}"

    @abstractmethod
    def calculate_salary(self) -> float:
        """Розрахувати зарплату за правилами відповідної посади."""


class Director(Employee):
    position = "Директор"

    def __init__(
        self,
        surname: str,
        first_name: str,
        patronymic: str,
        base_salary: float,
        teaching_experience: int,
        management_experience: int,
    ) -> None:
        super().__init__(surname, first_name, patronymic, base_salary)
        self.teaching_experience = teaching_experience
        self.management_experience = management_experience

    def calculate_salary(self) -> float:
        # Формула саме із завдання: ставка * педстаж / 50 + керстаж * 500.
        return (
            self.base_salary * self.teaching_experience / 50
            + self.management_experience * 500
        )


class Teacher(Employee):
    position = "Вчитель"

    def __init__(
        self,
        surname: str,
        first_name: str,
        patronymic: str,
        base_salary: float,
        teaching_experience: int,
    ) -> None:
        super().__init__(surname, first_name, patronymic, base_salary)
        self.teaching_experience = teaching_experience

    def calculate_salary(self) -> float:
        return self.base_salary * self.teaching_experience / 30


class Guard(Employee):
    position = "Охоронець"

    def __init__(
        self,
        surname: str,
        first_name: str,
        patronymic: str,
        base_salary: float,
        work_experience: int,
    ) -> None:
        super().__init__(surname, first_name, patronymic, base_salary)
        self.work_experience = work_experience

    def calculate_salary(self) -> float:
        return self.base_salary + self.work_experience * 250


@dataclass(frozen=True, slots=True)
class SchoolStatistics:
    """Знімок статистики. Його значення не змінюються після переведення."""

    total_students: int
    boys_percent: float
    girls_percent: float
    average_class_size: float
    largest_class_name: str
    largest_class_count: int
    smallest_class_name: str
    smallest_class_count: int


class School:
    """Одна модель школи використовується і для графіків, і для зарплат."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._classes: list[SchoolClass] = []
        self._employees: list[Employee] = []

    @property
    def classes(self) -> tuple[SchoolClass, ...]:
        return tuple(self._classes)

    @property
    def employees(self) -> tuple[Employee, ...]:
        return tuple(self._employees)

    def add_class(self, school_class: SchoolClass) -> None:
        if any(item.name == school_class.name for item in self._classes):
            raise ValueError(f"Клас {school_class.name} уже існує.")
        self._classes.append(school_class)

    def add_employee(self, employee: Employee) -> None:
        self._employees.append(employee)

    def all_students(self) -> Iterator[Student]:
        for school_class in self._classes:
            yield from school_class.students

    def statistics(self) -> SchoolStatistics:
        students = list(self.all_students())
        total = len(students)
        boys = sum(student.gender == "Хлопець" for student in students)
        girls = sum(student.gender == "Дівчина" for student in students)
        maximum = max(self._classes, key=lambda item: item.student_count, default=None)
        minimum = min(self._classes, key=lambda item: item.student_count, default=None)

        return SchoolStatistics(
            total_students=total,
            boys_percent=100 * boys / total if total else 0.0,
            girls_percent=100 * girls / total if total else 0.0,
            average_class_size=total / len(self._classes) if self._classes else 0.0,
            largest_class_name=maximum.name if maximum else "—",
            largest_class_count=maximum.student_count if maximum else 0,
            smallest_class_name=minimum.name if minimum else "—",
            smallest_class_count=minimum.student_count if minimum else 0,
        )

    def promote_one_year(self) -> int:
        """Випустити 11-ті класи й перевести інші. Повернути кількість випускників."""
        promoted_classes: list[SchoolClass] = []
        graduates = 0
        for school_class in self._classes:
            if school_class.parallel == 11:
                graduates += school_class.student_count
            else:
                school_class.promote()  # Виклик методу конкретного об'єкта класу.
                promoted_classes.append(school_class)

        self._classes = promoted_classes
        return graduates
