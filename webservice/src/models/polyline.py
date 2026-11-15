from bisect import bisect_left
from functools import cached_property
from typing import List
from typing import Sequence
from typing import Tuple

Coordinate = Sequence[float]
Vertex = Tuple[List[float], float]


class RoutePathProjection:
    def __init__(self, *, coordinates: List[List[float]], cumulative_distances: List[float], stop_distances: List[float]):
        self.coordinates: List[List[float]] = coordinates
        self.cumulative_distances: List[float] = cumulative_distances
        self.stop_distances: List[float] = stop_distances

    @property
    def start_distance(self) -> float:
        return self.stop_distances[0]

    @property
    def end_distance(self) -> float:
        return self.stop_distances[-1]

    @property
    def length(self) -> float:
        return self.end_distance - self.start_distance

    @cached_property
    def progress_vertices(self) -> List[Vertex]:
        return [(coordinate, self._progress_at(distance)) for coordinate, distance in self.trim()]

    def trim(self) -> List[Vertex]:
        return [self._vertex_at(self.start_distance), *self._inner_vertices(), self._vertex_at(self.end_distance)]

    def _progress_at(self, distance: float) -> float:
        return (distance - self.start_distance) / self.length

    def _vertex_at(self, distance: float) -> Vertex:
        return interpolate_coordinate(self.coordinates, self.cumulative_distances, distance), distance

    def _inner_vertices(self) -> List[Vertex]:
        return [
            (list(coordinate), distance)
            for coordinate, distance in zip(self.coordinates, self.cumulative_distances)
            if self.start_distance < distance < self.end_distance
        ]


def interpolate_coordinate(coordinates: Sequence[Coordinate], cumulative_distances: Sequence[float], distance: float) -> List[float]:
    index = bisect_left(cumulative_distances, distance, lo=1)
    if index == len(cumulative_distances):
        return list(coordinates[-1][:2])

    fraction = _fraction_between(cumulative_distances[index - 1], cumulative_distances[index], distance)

    return _interpolate_coordinate_pair(coordinates[index - 1], coordinates[index], fraction)


def _fraction_between(start_distance: float, end_distance: float, distance: float) -> float:
    segment_length = end_distance - start_distance
    if segment_length == 0:
        return 0.0

    return (distance - start_distance) / segment_length


def _interpolate_coordinate_pair(left: Coordinate, right: Coordinate, fraction: float) -> List[float]:
    return [left[0] + (right[0] - left[0]) * fraction, left[1] + (right[1] - left[1]) * fraction]
