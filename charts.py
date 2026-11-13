"""Чотири графіки для сценарію 1."""

from collections import Counter, defaultdict
from random import Random

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from models import School

BAR_COLOR = "#2875a7"
DOT_COLOR = "#ef7d3c"


def parallel_chart(school: School) -> Figure:
    """Стовпчики: загальна кількість учнів кожної паралелі."""
    counts: Counter[int] = Counter()
    for school_class in school.classes:
        counts[school_class.parallel] += school_class.student_count
    grades = sorted(counts)

    figure, ax = plt.subplots(figsize=(9, 4))
    ax.bar(grades, [counts[grade] for grade in grades], color=BAR_COLOR)
    ax.set_xticks(grades)
    ax.set_xlabel("Паралель")
    ax.set_ylabel("Кількість учнів")
    ax.set_title("Учні за паралелями")
    ax.grid(axis="y", alpha=0.2)
    figure.tight_layout()
    return figure


def vertical_chart(school: School) -> Figure:
    """Стовпчики: середній розмір класу для літер А, Б тощо."""
    sizes: defaultdict[str, list[int]] = defaultdict(list)
    for school_class in school.classes:
        sizes[school_class.letter].append(school_class.student_count)
    letters = sorted(sizes)
    averages = [sum(sizes[letter]) / len(sizes[letter]) for letter in letters]

    figure, ax = plt.subplots(figsize=(9, 4))
    ax.bar(letters, averages, color="#3b9b89")
    ax.set_xlabel("Вертикаль (літера класу)")
    ax.set_ylabel("Середня кількість учнів")
    ax.set_title("Середній розмір класу за вертикалями")
    ax.grid(axis="y", alpha=0.2)
    figure.tight_layout()
    return figure


def birth_year_chart(school: School) -> Figure:
    """Лінійний графік кількості учнів за роками народження."""
    counts = Counter(student.birth_year for student in school.all_students())
    years = sorted(counts)

    figure, ax = plt.subplots(figsize=(9, 4))
    ax.plot(years, [counts[year] for year in years], marker="o", color=BAR_COLOR)
    ax.set_xticks(years)
    ax.set_xlabel("Рік народження")
    ax.set_ylabel("Кількість учнів")
    ax.set_title("Кількість учнів за роком народження")
    ax.grid(alpha=0.2)
    figure.tight_layout()
    return figure


def grades_scatter_chart(school: School) -> Figure:
    """Scatter: кожна точка є середньою оцінкою окремого учня."""
    sorted_classes = sorted(school.classes, key=lambda item: (item.parallel, item.letter))
    rng = Random(41)  # Однаковий невеликий зсув точок під час кожного запуску.
    x: list[float] = []
    y: list[float] = []
    for index, school_class in enumerate(sorted_classes):
        for student in school_class.students:
            x.append(index + rng.uniform(-0.23, 0.23))
            y.append(student.average_grade)

    figure, ax = plt.subplots(figsize=(12, 5))
    ax.scatter(x, y, color=DOT_COLOR, s=19, alpha=0.55)
    ax.set_xticks(range(len(sorted_classes)))
    ax.set_xticklabels([item.name for item in sorted_classes], rotation=55, ha="right")
    ax.set_xlabel("Клас")
    ax.set_ylabel("Середня оцінка учня")
    ax.set_ylim(0, 12.5)
    ax.set_title("Залежність середньої оцінки від класу")
    ax.grid(axis="y", alpha=0.2)
    figure.tight_layout()
    return figure
