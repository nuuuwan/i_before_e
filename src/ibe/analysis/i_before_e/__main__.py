from pathlib import Path

from ibe.analysis.i_before_e.ErrorPlotMixin import ErrorPlotMixin
from ibe.core.Word import Word


class IBeforeEAnalysis(ErrorPlotMixin):
    GRAPH_FOLDER = Path("graphs")

    def __init__(self):
        self.words = Word.list()
        self.examples = []
        for word in self.words:
            for index in range(len(word) - 1):
                pair = word[index] + word[index + 1]
                if pair in ("ie", "ei"):
                    previous = word[index - 1] if index else None
                    self.examples.append((pair, previous))

    def analyze(self, exception):
        true_positive = sum(
            pair == "ei" and previous == exception
            for pair, previous in self.examples
        )
        true_negative = sum(
            pair == "ie" and previous != exception
            for pair, previous in self.examples
        )
        return true_positive + true_negative, len(self.examples) - (
            true_positive + true_negative
        )

    def results(self):
        results = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            candidate_words = sum(
                letter + "ie" in word or letter + "ei" in word
                for word in self.words
            )
            if candidate_words < 30:
                continue
            correct, incorrect = self.analyze(letter)
            accuracy = correct / (correct + incorrect)
            results.append((letter, accuracy, correct, incorrect))
        return sorted(results, key=lambda result: (-result[1], result[0]))

    @staticmethod
    def print_better_than_c(results):
        print("Exception letters that outperform C:\n")
        for rank, (letter, accuracy, correct, incorrect) in enumerate(
            results, start=1
        ):
            if letter == "c":
                break
            total = correct + incorrect
            print(
                f"{rank}. I before E except after {letter.upper()}: "
                f"{accuracy:.1%} ({correct}/{total})"
            )

    def run(self):
        results = self.results()
        self.GRAPH_FOLDER.mkdir(exist_ok=True)
        self.print_better_than_c(results)
        self.plot_all(results)
        print(f"\nGraphs written to {self.GRAPH_FOLDER}/")


IBeforeEAnalysis().run()
