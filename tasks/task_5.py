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
