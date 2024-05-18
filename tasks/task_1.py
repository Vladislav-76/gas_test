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
from pathlib import Path


FILEDIR = f"{Path(__file__).parent}/data_files/task_1/"
DELIMITER = "|"


"""
Реализация для файлов разумного размера.
Если строки файла не помещаются в питоновскую структуру данных,
реализация будет существенно сложнее с подключением БД.
"""


def get_uniq_rows(filename="file.csv"):
    with open(file=FILEDIR + filename, encoding="utf-8") as file:
        rows = csv.reader(file, delimiter=DELIMITER)
        columns = next(rows)
        print(columns)
        uniq_rows = set()
        for row in rows:
            uniq_rows.add(tuple(row))
    return uniq_rows, columns


if __name__ == "__main__":
    get_uniq_rows()

