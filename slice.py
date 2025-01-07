class Slice:
    _start_coordinates: list[float] = None
    _end_coordinates: list[float]
    _vertices: list[list[float]] = None
    _area: float = None
    _base: float = None
    _thickness: float = None
    _num_of_vertices: int = None

    def __init__(
            self,
            start_coordinates: list[float],
            end_coordinates: list[float],
            area: float,
            long_base: float
    ) -> None:
        if self._num_of_vertices is None:
            raise TypeError("Slice type not defined")
        self._start_coordinates = start_coordinates
        self._end_coordinates = end_coordinates
        self._area = area
        self._base = long_base
        self._make_slice()

    def _make_slice(self) -> None:
        pass

    def get_vertices(self) -> list[list[float]]:
        return self._vertices

    def mirror_horizontally(self, y: float) -> None:
        for i in range(self._num_of_vertices):
            self._vertices[i][1] = 2 * y - self._vertices[i][1]

    def transpose(self, x: float, y: float) -> None:
        for i in range(self._num_of_vertices):
            self._vertices[i][0] += x
            self._vertices[i][1] += y


class TriangleSlice(Slice):
    _height: float = None
    _num_of_vertices: int = 3

    def __init__(self, *args, triangle_height=None) -> None:
        self._height = triangle_height
        super().__init__(*args)


class StartTriangleSlice(TriangleSlice):
    def _make_slice(self) -> None:
        x0, y0 = self._start_coordinates
        x2, y2 = self._end_coordinates
        x1 = x0
        y1 = y0 + self._base
        self._vertices = [[x0, y0], [x1, y1], [x2, y2]]


class EndTriangleSlice(TriangleSlice):
    def _make_slice(self) -> None:
        x0, y0 = self._start_coordinates
        x2, y2 = self._end_coordinates
        x1 = x0
        y1 = y0 - self._base
        self._vertices = [[x0, y0], [x1, y1], [x2, y2]]


class CornerSlice(Slice):
    _corner_coordinates: list[float] = None
    _triangle_height: float = None
    _trapezoid_height: float = None
    _short_base: float = None
    _num_of_vertices: int = 5

    def __init__(self, *args, corner_coordinates=None, triangle_height=None, trapezoid_height=None,
                 short_base=None) -> None:
        self._corner_coordinates = corner_coordinates
        self._triangle_height = triangle_height
        self._trapezoid_height = trapezoid_height
        self._short_base = short_base
        super().__init__(*args)


class StartCornerSlice(CornerSlice):
    def _make_slice(self) -> None:
        x0, y0 = self._start_coordinates
        x1, y1 = self._corner_coordinates
        x4, y4 = self._end_coordinates
        y2 = y1
        x2 = self._base + y0 - y1 + x0
        x3 = x4 + self._short_base
        y3 = y4
        self._vertices = [[x0, y0], [x1, y1], [x2, y2], [x3, y3], [x4, y4]]


class EndCornerSlice(CornerSlice):
    def _make_slice(self) -> None:
        x0, y0 = self._start_coordinates
        x1, y1 = self._corner_coordinates
        x4, y4 = self._end_coordinates
        x2 = x1
        y2 = y1 - self._base + x1 - x0
        x3 = x4 + self._short_base
        y3 = y4
        self._vertices = [[x0, y0], [x1, y1], [x2, y2], [x3, y3], [x4, y4]]


class TwoCornerSlice(CornerSlice):
    _second_corner_coordinates: list[float] = None

    def __init__(self, *args, second_corner_coordinates=None, **kwargs) -> None:
        self._second_corner_coordinates = second_corner_coordinates
        super().__init__(*args, **kwargs)

    def _make_slice(self) -> None:
        x0, y0 = self._start_coordinates
        x1, y1 = self._corner_coordinates
        x2, y2 = self._second_corner_coordinates
        x4, y4 = self._end_coordinates
        x3 = x0
        y3 = y2
        self._vertices = [[x0, y0], [x1, y1], [x2, y2], [x3, y3], [x4, y4]]


class TrapezoidSlice(Slice):
    _height: float = None
    _short_base: float = None
    _num_of_vertices: int = 4

    def __init__(self, *args, trapezoid_height=None, short_base=None) -> None:
        self._height = trapezoid_height
        self._short_base = short_base
        super().__init__(*args)

    def _make_slice(self) -> None:
        x0, y0 = self._start_coordinates
        x3, y3 = self._end_coordinates
        x1 = x0 + self._base
        x2 = x3 + self._short_base
        y1 = y0
        y2 = y3
        self._vertices = [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
