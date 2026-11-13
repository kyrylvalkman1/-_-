"""Службовий генератор синтетичних прикладів; готові CSV вже додаються до проєкту."""
import csv
import random
from pathlib import Path

rng = random.Random(2026)
output = Path(__file__).parent / 'data'

last_names = [
    'Бондаренко', 'Левченко', 'Гончарук', 'Кравець', 'Дорошенко', 'Сидоренко',
    'Климчук', 'Федоренко', 'Романюк', 'Олійник', 'Марченко', 'Шевчук',
    'Литвин', 'Костенко', 'Паламарчук', 'Гаврилюк', 'Павленко', 'Семенюк',
    'Грищенко', 'Назаренко', 'Мельничук', 'Петрук', 'Ткаченко', 'Данилюк',
]
male_names = ['Максим', 'Андрій', 'Денис', 'Богдан', 'Назар', 'Марк', 'Тимофій', 'Матвій', 'Артем', 'Владислав']
female_names = ['Софія', 'Марія', 'Анна', 'Дарина', 'Олександра', 'Вікторія', 'Катерина', 'Злата', 'Ярина', 'Поліна']
male_patronymics = ['Олександрович', 'Ігорович', 'Сергійович', 'Андрійович', 'Романович', 'Михайлович']
female_patronymics = ['Олександрівна', 'Ігорівна', 'Сергіївна', 'Андріївна', 'Романівна', 'Михайлівна']

with (output / 'classes.csv').open('w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['class_id', 'parallel', 'letter'])
    for parallel in range(1, 12):
        for letter in ('А', 'Б'):
            writer.writerow([f'{parallel}-{letter}', parallel, letter])

with (output / 'students.csv').open('w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['class_id', 'surname', 'first_name', 'patronymic', 'birth_year', 'gender', 'average_grade'])
    for parallel in range(1, 12):
        for letter in ('А', 'Б'):
            # Вертикаль А має трохи більший середній розмір, щоб графік був показовим.
            count = rng.randint(20, 27) if letter == 'А' else rng.randint(15, 23)
            for _ in range(count):
                gender = rng.choice(('Хлопець', 'Дівчина'))
                first = rng.choice(male_names if gender == 'Хлопець' else female_names)
                patronymic = rng.choice(male_patronymics if gender == 'Хлопець' else female_patronymics)
                year = 2026 - parallel - 6 + rng.choice((-1, 0, 0, 0, 1))
                grade = round(rng.uniform(5.1, 11.8), 1)
                writer.writerow([f'{parallel}-{letter}', rng.choice(last_names), first, patronymic, year, gender, grade])
