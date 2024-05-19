"""
В наличии текстовый файл с набором русских слов(имена существительные, им.падеж)
Одна строка файла содержит одно слово.

Задание:
Написать программу которая выводит список слов,
каждый элемент списка которого - это новое слово,
которое состоит из двух сцепленных в одно, которые имеются в текстовом файле.
Порядок вывода слов НЕ имеет значения

Например, текстовый файл содержит слова:
ласты
стык
стыковка
баласт
кабала
карась

Пользователь вводмт первое слово: ласты
Программа выводит:
ластык
ластыковка

Пользователь вводмт первое слово: кабала
Программа выводит:
кабаласты
кабаласт

Пользователь вводмт первое слово: стыковка
Программа выводит:
стыковкабала
стыковкарась
"""


from pathlib import Path

FILEDIR = f"{Path(__file__).parent}/data_files/task_5/"
FILENAME = "words.txt"


def glued_words(word, file=FILEDIR + FILENAME):
    with open(file, encoding="utf-8") as file:
        for line in map(str.strip, file):
            if result := joined_word(word, line):
                yield result


def joined_word(word, linked_word):
    start_index = len(word) - min(len(word) - 1, len(linked_word) - 1)
    for i in range(start_index, len(word)):
        if word[i:] == linked_word[:len(word) - i]:
            return word + linked_word[len(word) - i:]


if __name__ == "__main__":
    while True:
        print(*glued_words(word=input()), sep="\n")
