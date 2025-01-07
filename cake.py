import copy
import math
# from typing import Dict

from slice import Slice, StartTriangleSlice, EndTriangleSlice, StartCornerSlice, EndCornerSlice, TwoCornerSlice, TrapezoidSlice

class Cake:
    _origin: list[float] = None
    _vertices: list[list[float]] = None
    _long_side: float = None
    _short_side: float = None
    _perimeter: float = None
    _area: float = None
    _trapezoid_height: float = None

    _num_of_slices: int = None

    _slice_area: float = None
    _long_base: float = None
    _short_base: float = None
    _triangle_height: float = None

    _slices: list[Slice] = None

    _start_corner_slice_base: float | None = None
    _end_corner_slice_base: float | None = None

    def __init__(self, long_side, short_side, origin = (0,0), can_swap_sides = False) -> None:
        if short_side > long_side:
            if can_swap_sides:
                self._long_side = short_side
                self._short_side = long_side
            else:
                raise ValueError("short_side is greater than or equal to long_side")
        else:
            self._long_side = long_side
            self._short_side = short_side
        self._origin = origin
        self._area = self._long_side*self._short_side
        self._perimeter = 2*(self._long_side + self._short_side)
        self._trapezoid_height = self._short_side/2
        self._find_vertices()

    def get_origin(self) -> list[float]:
        return self._origin

    def get_vertices(self) -> list[list[float]]:
        return self._vertices

    def get_slice_vertices(self) -> list[list[list[float]]]:
        slice_vertices: list[list[list[float]]] = []
        for cake_slice in self._slices:
            slice_vertices.append(cake_slice.get_vertices())
        return slice_vertices

    def _find_vertices(self) -> None:
        x, y = self._origin
        x2 = x + self._long_side
        y2 = y + self._short_side
        self._vertices = [[x,y],[x,y2],[x2,y2],[x2,y]]

    def slice(self, num_of_slices) -> None:
        if not isinstance(num_of_slices, int):
            raise TypeError ("num_of_slices must be an integer")
        if num_of_slices < 3:
            raise ValueError("num_of_slices must be greater than 2")
        self._num_of_slices = num_of_slices
        self._slice_area = self._area/self._num_of_slices
        self._long_base = self._perimeter/self._num_of_slices
        self._short_base = 2*(self._long_side - self._short_side)/self._num_of_slices
        self._triangle_height = 2*self._slice_area/self._long_base
        self._make_slices()

    def _make_slices(self) -> None:
        # Make half of start triangles if any
        self._slices = []
        x_min: float
        x_max: float
        y_min: float
        Y_max: float
        x_min, y_min = self._origin
        x_max, y_max = self._vertices[2]
        y_mid = y_min + self._trapezoid_height
        x: float = x_min
        y: float = y_min + self._trapezoid_height
        l: float | None = x_min + self._triangle_height
        num_of_subslices: int
        remainder: int

        side: int = 0
        for i in range (math.ceil(self._num_of_slices/2)):
            match side:
                case 0:
                    difference = y_max - y
                    if difference >= self._long_base: # triangle
                        self._slices.append(StartTriangleSlice(
                            (x, y),
                            (l, y_mid),
                            self._slice_area,
                            self._long_base,
                            triangle_height=self._triangle_height
                        ))
                        y += self._long_base
                        if difference == self._long_base:
                            self._start_corner_slice_base = 0
                            side = 1
                    elif difference > 0: # corner
                        self._start_corner_slice_base = self._find_corner_length(difference)
                        self._slices.append(StartCornerSlice(
                            (x, y),
                            (l, y_mid),
                            self._slice_area,
                            self._long_base,
                            corner_coordinates=(x_min, y_max),
                            triangle_height=self._triangle_height,
                            trapezoid_height=self._trapezoid_height,
                            short_base=self._start_corner_slice_base
                        ))
                        y = y_max
                        x += self._long_base - difference
                        l += self._start_corner_slice_base
                        side = 1
                case 1:
                    difference = x_max - x
                    if difference >= self._long_base: # trapezoid
                        self._slices.append(TrapezoidSlice(
                            (x, y),
                            (l, y_mid),
                            self._slice_area,
                            self._long_base,
                            trapezoid_height=self._trapezoid_height,
                            short_base=self._short_base
                        ))
                        x += self._long_base
                        l += self._short_base
                        if difference == self._long_base:
                            self._end_corner_slice_base = 0
                            side = 2
                    elif difference > 0: # corner
                        self._end_corner_slice_base = x_max - l - self._triangle_height
                        args = (
                            (x, y),
                            (l, y_mid),
                            self._slice_area,
                            self._long_base,
                        )
                        kwargs = {
                            "corner_coordinates": (x_max, y_max),
                            "triangle_height": self._triangle_height,
                            "trapezoid_height": self._trapezoid_height,
                            "short_base": self._end_corner_slice_base
                        }
                        if self._long_base > difference + self._short_side:
                            self._slices.append(TwoCornerSlice(
                                *args,
                                second_corner_coordinates=(x_max,y_min),
                                **kwargs
                            ))
                        else:
                            self._slices.append(EndCornerSlice(*args, **kwargs))
                        x = x_max
                        y -= self._long_base - difference
                        l += self._end_corner_slice_base
                        side = 2
                case 2:
                    self._slices.append(EndTriangleSlice(
                        (x, y),
                        (l, y_mid),
                        self._slice_area,
                        self._long_base,
                        triangle_height=self._triangle_height
                    ))
                    y -= self._long_base

        # mirror all slices except middle slice (index = 0:floor(n/2))
        for i in range(math.floor(self._num_of_slices/2)):
            cake_slice = copy.deepcopy(self._slices[i])
            cake_slice.mirror_horizontally(y_min + self._trapezoid_height)
            self._slices.append(cake_slice)

    def _find_corner_length(self, short_side_base: float) -> float:
        long_side_base: float = self._long_base - short_side_base
        return (
                2*(self._slice_area - 0.5*short_side_base*self._triangle_height)/self._trapezoid_height
                - long_side_base
        )

    def _find_middle_slice_corner_length(self, short_side_base: float, long_side_base: float) -> float:
        return (
                2*(self._slice_area - long_side_base*self._trapezoid_height)/short_side_base
        )

    def transpose(self, x, y) -> None:
        self._origin = [self._origin[0] + x, self._origin[1] + y]
        self._find_vertices()
        for cake_slice in self._slices:
            cake_slice.transpose(x,y)