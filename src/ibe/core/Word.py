from pathlib import Path


class Word:

    @staticmethod
    def list():
        WORDS_FILE_PATH = Path("data") / "words.txt"
        with open(WORDS_FILE_PATH, "r") as file:
            return [line.strip() for line in file]
