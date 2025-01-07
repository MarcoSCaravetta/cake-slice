import copy
import math
from typing import Dict

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

    def __init__(
            self,
            long_side: float,
            short_side: float,
            origin: list[float] = (0,0),
            can_swap_sides: bool = False
    ) -> None:
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
        self._slices = []
        x_min, y_min = self._origin
        x_max, y_max = self._vertices[2]
        y_mid = y_min + self._trapezoid_height # center y coordinate of current slice
        x = x_min # x coordinate of current slice
        y = y_min + self._trapezoid_height # y coordinate of current slice
        l = x_min + self._triangle_height # center x coordinate of current slice
        side: int = 0 # current side of cake

        # create fist ceiling(n/2) slices
        for i in range (math.ceil(self._num_of_slices/2)):
            match side:
                case 0: # 1st side
                    difference = y_max - y
                    if difference >= self._long_base: # triangle slice
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
                    elif difference > 0: # 1st corner slice
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
                case 1: # 2nd side, i.e. the top
                    difference = x_max - x
                    if difference >= self._long_base: # trapezoid slice
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
                    elif difference > 0: # 2nd corner slice
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
                        if self._long_base > difference + self._short_side: # two corner slice
                            self._slices.append(TwoCornerSlice(
                                *args,
                                second_corner_coordinates=(x_max,y_min),
                                **kwargs
                            ))
                        else: # regular corner slice
                            self._slices.append(EndCornerSlice(*args, **kwargs))
                        x = x_max
                        y -= self._long_base - difference
                        l += self._end_corner_slice_base
                        side = 2
                case 2: # 3rd side
                    self._slices.append(EndTriangleSlice(
                        (x, y),
                        (l, y_mid),
                        self._slice_area,
                        self._long_base,
                        triangle_height=self._triangle_height
                    ))
                    y -= self._long_base

        # create remaining floor(n/2) slices by mirroring the first floor(n/2) slices
        for i in range(math.floor(self._num_of_slices/2)):
            cake_slice = copy.deepcopy(self._slices[i])
            cake_slice.mirror_horizontally(y_min + self._trapezoid_height)
            self._slices.append(cake_slice)

    def _find_corner_length(self, short_side_base: float) -> float:
        long_side_base = self._long_base - short_side_base
        return (
                2*(self._slice_area - 0.5*short_side_base*self._triangle_height)/self._trapezoid_height
                - long_side_base
        )

    def transpose(self, x: float = 0, y: float = 0) -> None:
        self._origin = [self._origin[0] + x, self._origin[1] + y]
        self._find_vertices()
        for cake_slice in self._slices:
            cake_slice.transpose(x,y)