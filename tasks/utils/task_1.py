import csv
from datetime import date
from pathlib import Path
from random import choice, randint

from faker import Faker

FILEDIR = f"{Path(__file__).resolve().parents[1]}/data_files/task_1/"
COLUMNS = ("lastname", "name", "patronymic", "date_of_birth", "id")
DELIMITER = "|"
DATE_PATTERN = "%d.%m.%Y"
ID_FORMAT = ((100000000, 999999999), (1000, 9999))


def create_fake_file(filename="file.csv", lines=100, date_start=date(1900, 1, 1), date_end=date.today()):
    with open(file=FILEDIR + filename, mode="w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=DELIMITER)
        writer.writerow(COLUMNS)
        rows = [fake_row(date_start, date_end, DATE_PATTERN) for _ in range(lines)]
        rows.extend(make_duplicates(rows, 20))
        rows.extend(make_rows_with_same_id(rows, 20, date_start, date_end, DATE_PATTERN))
        writer.writerows(rows)


def fake_row(date_start, date_end, date_pattern):
    fake = Faker("ru_RU")
    names = choice((
        (fake.last_name_male, fake.first_name_male, fake.middle_name_male),
        (fake.last_name_female, fake.first_name_female, fake.middle_name_female),
    ))
    lastname, name, patronymic = (name() for name in names)
    date_of_birth = fake.date_between_dates(date_start, date_end).strftime(date_pattern)
    person_id = f"{randint(*ID_FORMAT[0])}-{randint(*ID_FORMAT[1])}"
    return lastname, name, patronymic, date_of_birth, person_id


def make_duplicates(rows, amount):
    return (choice(rows) for _ in range(amount))


def make_rows_with_same_id(rows, amount, date_start, date_end, date_pattern):
    result = []
    for _ in range(amount):
        person_id = choice(rows)[-1]
        row = list(fake_row(date_start, date_end, date_pattern))
        row[-1] = person_id
        result.append(row)
    return result


if __name__ == "__main__":
    create_fake_file()
