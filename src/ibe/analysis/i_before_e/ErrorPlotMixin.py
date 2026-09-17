import matplotlib.pyplot as plt


class ErrorPlotMixin:

    def error_rate(self, label, pair, matches_exception):
        errors = sum(
            example_pair == pair
            and (previous == label.lower()) is matches_exception
            for example_pair, previous in self.examples
        )
        return errors / len(self.examples) * 100

    @staticmethod
    def add_bars(axes, labels, false_positives, false_negatives):
        positive_bars = axes.bar(
            labels,
            false_positives,
            color="#d1495b",
            label="False positive",
        )
        negative_bars = axes.bar(
            labels,
            false_negatives,
            bottom=false_positives,
            color="#287271",
            label="False negative",
        )
        for label, positive, negative in zip(
            labels, positive_bars, negative_bars
        ):
            opacity = 0.25 if label == "C" else 1
            positive.set_alpha(opacity)
            negative.set_alpha(opacity)

    def plot_all(self, results):
        labels = [result[0].upper() for result in results]
        false_positives = [
            self.error_rate(label, "ie", True) for label in labels
        ]
        false_negatives = [
            self.error_rate(label, "ei", False) for label in labels
        ]
        figure, axes = plt.subplots(figsize=(11, 5))
        self.add_bars(axes, labels, false_positives, false_negatives)
        c_accuracy = next(result[1] for result in results if result[0] == "c")
        axes.axhline(
            (1 - c_accuracy) * 100,
            color="#333333",
            linewidth=0.8,
            linestyle="--",
        )
        axes.set(
            xlabel="Exception letter",
            ylabel="Error rate (%)",
            ylim=(0, 40),
        )
        axes.set_title("Errors produced by each exception letter")
        axes.legend(frameon=False)
        figure.tight_layout()
        figure.savefig(
            self.GRAPH_FOLDER / "all_exception_letters.png", dpi=180
        )
        plt.close(figure)
