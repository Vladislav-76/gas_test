# Имеется папка с файлами
# Реализовать удаление файлов старше N дней


import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

DIR_PATH = f"{Path(__file__).parent}/data_files/task_4/"
OLDER_THEN_DAYS = 5
FROM_MODIFY = True  # Если True, отсчет с момента изменения файлов, иначе с момента создания
LOG_FILE = "old_file_removing.log"

logging.basicConfig(
    level=logging.INFO,
    filename=DIR_PATH + LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def old_file_removing(dir_path=DIR_PATH):
    for _, _, files in os.walk(dir_path):
        for file in files:
            file_path = dir_path + file
            if os.path.isfile(file_path):
                stat_result = os.stat(file_path)
                starting_time = stat_result.st_mtime if FROM_MODIFY else stat_result.st_ctime
                file_age = datetime.today() - datetime.fromtimestamp(starting_time)
                if file_age > timedelta(days=OLDER_THEN_DAYS) and file != LOG_FILE:
                    try:
                        os.remove(file_path)
                        logging.info(f"Файл {file_path} удалён успешно.")
                    except Exception as error:
                        logging.error(error)


if __name__ == "__main__":
    old_file_removing()
