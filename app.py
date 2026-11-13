"""Сценарій 1: вебсторінка зі статистикою та переведенням класів.

Запуск: python -m streamlit run app.py
"""

import matplotlib.pyplot as plt
import streamlit as st

from charts import birth_year_chart, grades_scatter_chart, parallel_chart, vertical_chart
from data_loader import load_school
from models import School, SchoolStatistics

st.set_page_config(page_title="Школа — залікова робота", page_icon="🏫", layout="wide")


def show_statistics(stats: SchoolStatistics) -> None:
    """Показати всі п'ять статистичних показників із завдання."""
    col1, col2, col3 = st.columns(3)
    col1.metric("Усього учнів", stats.total_students)
    col2.metric("Хлопців", f"{stats.boys_percent:.1f} %")
    col3.metric("Дівчат", f"{stats.girls_percent:.1f} %")
    st.write(f"**Середня кількість учнів у класі:** {stats.average_class_size:.2f}")
    st.write(
        f"**Найбільше учнів:** {stats.largest_class_count} — клас {stats.largest_class_name}"
    )
    st.write(
        f"**Найменше учнів:** {stats.smallest_class_count} — клас {stats.smallest_class_name}"
    )


def show_charts(school: School) -> None:
    """Побудувати та показати 4 потрібні графіки."""
    st.subheader("Графіки")
    first_column, second_column = st.columns(2)
    with first_column:
        figure = parallel_chart(school)
        st.pyplot(figure)
        plt.close(figure)
        figure = birth_year_chart(school)
        st.pyplot(figure)
        plt.close(figure)
    with second_column:
        figure = vertical_chart(school)
        st.pyplot(figure)
        plt.close(figure)
        figure = grades_scatter_chart(school)
        st.pyplot(figure)
        plt.close(figure)


def show_class_table(school: School) -> None:
    rows = [
        {"Клас": item.name, "Паралель": item.parallel,
         "Вертикаль": item.letter, "Кількість учнів": item.student_count}
        for item in sorted(school.classes, key=lambda item: (item.parallel, item.letter))
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)


# Об'єкт школи не створюється заново під час кожного натискання кнопки.
if "school" not in st.session_state:
    st.session_state.school = load_school()
    st.session_state.promoted = False
    st.session_state.before_stats = None
    st.session_state.graduates = 0

school: School = st.session_state.school
st.title("🏫 Моя школа: статистика та класи")
st.caption("Заліковий проєкт із програмування • Python / ООП / CSV / Streamlit")

with st.sidebar:
    st.header("Керування")
    st.write(f"Школа: **{school.name}**")
    st.write(f"Класів зараз: **{len(school.classes)}**")
    st.write(f"Працівників у моделі: **{len(school.employees)}**")
    if st.button("↻ Повернути початкові CSV-дані", use_container_width=True):
        st.session_state.school = load_school()
        st.session_state.promoted = False
        st.session_state.before_stats = None
        st.session_state.graduates = 0
        st.rerun()

st.header("Сценарій 1. Статистика")
show_statistics(school.statistics())

st.subheader("Усі класи")
show_class_table(school)

st.divider()
st.header("Переведення на наступний рік")
if st.button("Перевести всі класи на рік вперед", disabled=st.session_state.promoted):
    st.session_state.before_stats = school.statistics()
    st.session_state.graduates = school.promote_one_year()
    st.session_state.promoted = True
    st.rerun()

if st.session_state.promoted:
    old: SchoolStatistics = st.session_state.before_stats
    new = school.statistics()
    st.success(
        f"Переведення виконано. Випущено {st.session_state.graduates} учнів 11-х класів. "
        "Усі інші класи перейшли на одну паралель вище."
    )
    st.write("**Перевірка:** паралелі 1 немає, паралелі 11 з минулих 10-х класів є, "
             "12-ї паралелі немає.")
    st.subheader("Порівняння статистики до й після")
    st.dataframe([
        {"Показник": "Загальна кількість учнів", "До": old.total_students,
         "Після": new.total_students},
        {"Показник": "Хлопці, %", "До": f"{old.boys_percent:.2f}",
         "Після": f"{new.boys_percent:.2f}"},
        {"Показник": "Дівчата, %", "До": f"{old.girls_percent:.2f}",
         "Після": f"{new.girls_percent:.2f}"},
        {"Показник": "Середній розмір класу", "До": f"{old.average_class_size:.2f}",
         "Після": f"{new.average_class_size:.2f}"},
        {"Показник": "Найбільший клас", "До": f"{old.largest_class_name}: {old.largest_class_count}",
         "Після": f"{new.largest_class_name}: {new.largest_class_count}"},
        {"Показник": "Найменший клас", "До": f"{old.smallest_class_name}: {old.smallest_class_count}",
         "Після": f"{new.smallest_class_name}: {new.smallest_class_count}"},
    ], use_container_width=True, hide_index=True)

st.divider()
show_charts(school)
st.caption("Сценарій 2 запускається окремо в терміналі: python salary_cli.py")
