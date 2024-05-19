# имеется текстовый файл file.csv, в котром разделитель полей с данными: | (верт. черта)
# пример ниже содержит небольшую часть этого файла(начальные 3 строки, включая строку заголовков полей)
"""
lastname|name|patronymic|date_of_birth|id
Фамилия1|Имя1|Отчество1 |21.11.1998 |312040348-3048
Фамилия2|Имя2|Отчество2 |11.01.1972 |457865234-3431
...
"""
# Задание
# 1 Реализовать сбор уникальных записей
# 2 Случается, что под одиннаковым id присутствуют разные данные - собрать отдельно такие записи


import csv
from collections import defaultdict
from pathlib import Path

FILEDIR = f"{Path(__file__).parent}/data_files/task_1/"
DELIMITER = "|"


class NoIdError(Exception):
    pass


"""
Реализация для файлов разумного размера.
Если строки файла не помещаются в питоновскую структуру данных,
реализация будет сложнее.
"""


def get_uniq_rows(filename="file.csv"):
    with open(file=FILEDIR + filename, encoding="utf-8") as file:
        rows = csv.reader(file, delimiter=DELIMITER)
        columns = next(rows)
        uniq_rows = set()
        for row in rows:
            uniq_rows.add(tuple(row))
    return uniq_rows, columns


def write_uniq_rows(filename="uniq_rows.csv"):
    uniq_rows, columns = get_uniq_rows()
    with open(file=FILEDIR + filename, mode="w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=DELIMITER)
        writer.writerow(columns)
        writer.writerows(uniq_rows)


def get_multiply_rows_with_same_id(filename="file.csv"):
    uniq_rows, columns = get_uniq_rows(filename)
    if "id" in columns:
        id_index = columns.index("id")
    else:
        raise NoIdError("В файле отсутствует колонка id")
    rows_by_id = defaultdict(list)
    for row in map(list, uniq_rows):
        rows_by_id[list(row).pop(id_index)].append(row)
    filtered_rows = []
    for row_id, rows in rows_by_id.items():
        if len(rows_by_id[row_id]) > 1:
            for row in rows:
                row.insert(id_index, row_id)
                filtered_rows.append(row)
    return filtered_rows, columns


def write_multiply_rows_with_same_id(filename="multiply_rows_with_same_id.csv"):
    multiply_rows, columns = get_multiply_rows_with_same_id()
    with open(file=FILEDIR + filename, mode="w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=DELIMITER)
        writer.writerow(columns)
        writer.writerows(multiply_rows)


if __name__ == "__main__":
    write_uniq_rows()
    write_multiply_rows_with_same_id()
