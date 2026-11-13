"""Сценарій 2: командний рядок + вивантаження зарплат у CSV.

Запуск: python salary_cli.py
"""

import csv
from pathlib import Path

from data_loader import load_school
from models import Employee, School

OUTPUT_FILE = Path(__file__).resolve().parent / "salary.csv"


def export_salaries(school: School, destination: Path = OUTPUT_FILE) -> None:
    """Обчислити зарплати поліморфним методом та записати у CSV."""
    with destination.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Посада", "ПІБ", "Базова ставка", "Розрахована зарплата"])

        # Для всіх посад використовується той самий виклик calculate_salary().
        for employee in school.employees:
            worker: Employee = employee
            calculated = worker.calculate_salary()
            writer.writerow([
                worker.position,
                worker.full_name,
                f"{worker.base_salary:.2f}",
                f"{calculated:.2f}",
            ])


def main() -> None:
    school = load_school()  # Та сама модель і той самий завантажувач, що й у Streamlit.
    export_salaries(school)
    print(f"\nЗарплати працівників школи «{school.name}»\n")
    for employee in school.employees:
        print(
            f"{employee.position:<10} | {employee.full_name:<34} | "
            f"{employee.calculate_salary():>9.2f} грн"
        )
    print(f"\nТаблицю збережено у файл: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
