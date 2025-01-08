import matplotlib.patches
import matplotlib.pyplot


class CakeDrawer:
    _figure: matplotlib.pyplot.Figure = None
    _axes: matplotlib.pyplot.Axes = None

    def __init__(self) -> None:
        self._figure, self._axes = matplotlib.pyplot.subplots()

    def plot(self, coordinates: list[list[float]]) -> None:
        polygon = matplotlib.patches.Polygon(coordinates, edgecolor='k', facecolor='w')
        self._axes.add_patch(polygon)

    def plot_multiple(self, multiple_coordinates: list[list[list[float]]]) -> None:
        for coordinates in multiple_coordinates:
            polygon = matplotlib.patches.Polygon(coordinates, edgecolor='k', facecolor='w')
            self._axes.add_patch(polygon)

    @staticmethod
    def set_scale(x_min: float, x_max: float, y_min: float, y_max: float) -> None:
        matplotlib.pyplot.ylim([x_min, x_max])
        matplotlib.pyplot.ylim([y_min, y_max])
        matplotlib.pyplot.axis('equal')

    @staticmethod
    def add_text(x: float, y: float, text: str) -> None:
        matplotlib.pyplot.text(x, y, text)

    @staticmethod
    def show_plot() -> None:
        matplotlib.pyplot.xticks([])
        matplotlib.pyplot.yticks([])
        matplotlib.pyplot.show()
