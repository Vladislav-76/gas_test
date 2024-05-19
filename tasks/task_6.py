"""
Имеется банковское API возвращающее JSON
{
    "Columns": ["key1", "key2", "key3"],
    "Description": "Банковское API каких-то важных документов",
    "RowCount": 2,
    "Rows": [
        ["value1", "value2", "value3"],
        ["value4", "value5", "value6"]
    ]
}
Основной интерес представляют значения полей "Columns" и "Rows",
которые соответственно являются списком названий столбцов и значениями столбцов
Задание:
1 Получить JSON из внешнего API
ендпоинт: GET https://api.gazprombank.ru/very/important/docs?documents_date={"начало дня
сегодня в виде таймстемп"}
2 Валидировать входящий JSON используя модель pydantic
(из ТЗ известно что поле "key1" имеет тип int, "key2"(datetime), "key3"(str))
2 Представить данные "Columns" и "Rows" в виде плоского csv-подобного pandas.DataFrame
3 В полученном DataFrame произвести переименование полей по след. маппингу
"key1" -> "document_id", "key2" -> "document_dt", "key3" -> "document_name"
3 Полученный DataFrame обогатить доп. столбцом:
"load_dt" -> значение "сейчас"(датавремя)
"""


import logging
from collections import namedtuple
from datetime import datetime
from pathlib import Path

import pandas
import requests
from pydantic import BaseModel, ValidationError
from requests.exceptions import ConnectTimeout

DIR_PATH = f"{Path(__file__).parent}/data_files/task_6/"
LOG_FILE = "get_important_documents.log"
API_URL = "https://api.gazprombank.ru/very/important/docs"
FIELD_NAMES = namedtuple("FIELD_NAMES", ("columns", "rows"))("Columns", "Rows")
API_DATA_MOCK = {
    "Columns": ["key1", "key2", "key3"],
    "Description": "Банковское API каких-то важных документов",
    "RowCount": 4,
    "Rows": [
        ["value1", "value2", "value3"],
        ["value4", "value5", "value6"],
        [54, datetime.utcnow(), "value54"],
        [102, datetime.utcnow(), "value102"],
    ]
}

logging.basicConfig(
    level=logging.ERROR,
    filename=DIR_PATH + LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class VeryImportantDocument(BaseModel):
    key1: int
    key2: datetime
    key3: str


def get_documents_from_api(url=API_URL):
    day_start = datetime.combine(datetime.utcnow(), datetime.utcnow().min.time())
    params = {"documents_date": day_start.timestamp()}
    try:
        response = requests.get(url, params=params, timeout=1)
        if response.status_code == requests.codes.ok:
            data = response.json()
        else:
            logging.error(f"Ошибка доступа к API: {response.status_code}")
            response.raise_for_status()
    except ConnectTimeout as error:
        logging.error(error)
        data = API_DATA_MOCK  # Поскольку указанный в задании эндпойнт не отвечает, мокаем ответ
    return data


def validated_documents(data):
    validated_documents = []
    for row in data[FIELD_NAMES.rows]:
        try:
            VeryImportantDocument(**dict(zip(data[FIELD_NAMES.columns], row)))
            validated_documents.append(row)
        except ValidationError as error:
            logging.error(f"Ошибка валидации строки:\n{row}\n{error}")
    return validated_documents


def main():
    # 1 Получить JSON из внешнего API
    data = get_documents_from_api()

    # 2 Валидировать входящий JSON используя модель pydantic
    documents = validated_documents(data)

    # 2 Представить данные "Columns" и "Rows" в виде плоского csv-подобного pandas.DataFrame
    df = pandas.DataFrame(documents, columns=data[FIELD_NAMES.columns])

    # 3 В полученном DataFrame произвести переименование полей
    new_columns_names = ("document_id", "document_dt", "document_name")
    df = df.rename(columns=dict(zip(data[FIELD_NAMES.columns], new_columns_names)))

    # 3 Полученный DataFrame обогатить доп. столбцом:
    df["load_dt"] = datetime.utcnow()


if __name__ == "__main__":
    main()
