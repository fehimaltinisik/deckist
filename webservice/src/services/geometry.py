import math
from dataclasses import dataclass
from typing import Callable
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Tuple

from src.models.polyline import Coordinate
from src.models.polyline import RoutePathProjection

EARTH_RADIUS_IN_METERS: float = 6371000.0
METERS_PER_DEGREE: float = math.radians(1) * EARTH_RADIUS_IN_METERS

PlanarPoint = Tuple[float, float]


@dataclass(frozen=True)
class ProjectionTolerance:
    max_stop_offset_in_meters: float = 200.0
    lookahead_in_meters: float = 1500.0
    max_outlier_stop_ratio: float = 0.1


DEFAULT_PROJECTION_TOLERANCE: ProjectionTolerance = ProjectionTolerance()


def project_stops_onto_route_path(
        stop_coordinates: Sequence[Coordinate],
        route_path_coordinates: Sequence[Coordinate],
        tolerance: ProjectionTolerance = DEFAULT_PROJECTION_TOLERANCE
) -> Optional[RoutePathProjection]:
    if _has_too_few_points(stop_coordinates, route_path_coordinates):
        return None

    route_line = _PlanarRouteLine(route_path_coordinates)
    stop_distances = _StopLocator(route_line, tolerance).locate(stop_coordinates)
    if stop_distances is None or not _runs_forward(stop_distances):
        return None

    return RoutePathProjection(
        coordinates=route_line.coordinates,
        cumulative_distances=route_line.cumulative_distances,
        stop_distances=stop_distances
    )


class _SegmentMatch(NamedTuple):
    segment_index: int
    distance: float
    offset: float
    offset_at_distance: float


_OffsetSelector = Callable[[_SegmentMatch], float]


class _PlanarRouteLine:
    def __init__(self, coordinates: Sequence[Coordinate]):
        self.coordinates: List[List[float]] = [list(coordinate[:2]) for coordinate in coordinates]
        self.longitude_scale: float = math.cos(math.radians(coordinates[0][1]))
        self.points: List[PlanarPoint] = [self.to_planar(coordinate) for coordinate in coordinates]
        self.cumulative_distances: List[float] = _cumulative_distances(self.points)

    @property
    def segment_count(self) -> int:
        return len(self.points) - 1

    def to_planar(self, coordinate: Coordinate) -> PlanarPoint:
        return coordinate[0] * METERS_PER_DEGREE * self.longitude_scale, coordinate[1] * METERS_PER_DEGREE

    def distance_at(self, segment_index: int) -> float:
        return self.cumulative_distances[segment_index]

    def match_segment(self, point: PlanarPoint, segment_index: int, min_distance: float) -> _SegmentMatch:
        start_distance = self.distance_at(segment_index)
        segment_length = self.distance_at(segment_index + 1) - start_distance
        start, end = self.points[segment_index], self.points[segment_index + 1]
        fraction = _project_fraction(point, start, end)
        forward_fraction = max(fraction, _fraction_along(min_distance - start_distance, segment_length))

        return _SegmentMatch(
            segment_index=segment_index,
            distance=start_distance + forward_fraction * segment_length,
            offset=math.dist(point, _interpolate_point(start, end, fraction)),
            offset_at_distance=math.dist(point, _interpolate_point(start, end, forward_fraction))
        )


class _StopLocator:
    def __init__(self, route_line: _PlanarRouteLine, tolerance: ProjectionTolerance):
        self.route_line: _PlanarRouteLine = route_line
        self.tolerance: ProjectionTolerance = tolerance
        self.segment_index: int = 0
        self.previous_distance: float = 0.0
        self.outlier_count: int = 0

    def locate(self, stop_coordinates: Sequence[Coordinate]) -> Optional[List[float]]:
        last_stop_index = len(stop_coordinates) - 1
        stop_distances: List[float] = []
        for stop_index, stop_coordinate in enumerate(stop_coordinates):
            is_end_stop = stop_index in (0, last_stop_index)
            if not self._locate_stop(stop_coordinate, is_end_stop):
                return None
            stop_distances.append(self.previous_distance)

        if self._has_too_many_outliers(len(stop_coordinates)):
            return None

        return stop_distances

    def _locate_stop(self, stop_coordinate: Coordinate, is_end_stop: bool) -> bool:
        offset_of = _offset_at_distance if is_end_stop else _perpendicular_offset
        match = self._find_nearest_match_ahead(self.route_line.to_planar(stop_coordinate), offset_of)
        if self._is_within_max_offset(offset_of(match)):
            self._advance_to(match)
            return True

        self.outlier_count += 1

        return not is_end_stop

    def _find_nearest_match_ahead(self, point: PlanarPoint, offset_of: _OffsetSelector) -> _SegmentMatch:
        best = self._match(point, self.segment_index)
        for segment_index in range(self.segment_index + 1, self.route_line.segment_count):
            if self._is_beyond_lookahead(segment_index, best, offset_of):
                break
            match = self._match(point, segment_index)
            if offset_of(match) < offset_of(best):
                best = match

        return best

    def _match(self, point: PlanarPoint, segment_index: int) -> _SegmentMatch:
        return self.route_line.match_segment(point, segment_index, self.previous_distance)

    def _is_beyond_lookahead(self, segment_index: int, best: _SegmentMatch, offset_of: _OffsetSelector) -> bool:
        distance_past_best = self.route_line.distance_at(segment_index) - best.distance

        return self._is_within_max_offset(offset_of(best)) and distance_past_best > self.tolerance.lookahead_in_meters

    def _is_within_max_offset(self, offset: float) -> bool:
        return offset <= self.tolerance.max_stop_offset_in_meters

    def _advance_to(self, match: _SegmentMatch) -> None:
        self.segment_index = match.segment_index
        self.previous_distance = match.distance

    def _has_too_many_outliers(self, stop_count: int) -> bool:
        return self.outlier_count > self.tolerance.max_outlier_stop_ratio * stop_count


def _perpendicular_offset(match: _SegmentMatch) -> float:
    return match.offset


def _offset_at_distance(match: _SegmentMatch) -> float:
    return match.offset_at_distance


def _has_too_few_points(stop_coordinates: Sequence[Coordinate], route_path_coordinates: Sequence[Coordinate]) -> bool:
    return len(stop_coordinates) < 2 or len(route_path_coordinates) < 2


def _runs_forward(stop_distances: List[float]) -> bool:
    return stop_distances[-1] > stop_distances[0]


def _cumulative_distances(points: List[PlanarPoint]) -> List[float]:
    distances: List[float] = [0.0]
    for left, right in zip(points, points[1:]):
        distances.append(distances[-1] + math.dist(left, right))

    return distances


def _project_fraction(point: PlanarPoint, start: PlanarPoint, end: PlanarPoint) -> float:
    dx, dy = end[0] - start[0], end[1] - start[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return 0.0

    return _clamp_to_unit(((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared)


def _fraction_along(distance: float, segment_length: float) -> float:
    if segment_length == 0:
        return 0.0

    return _clamp_to_unit(distance / segment_length)


def _interpolate_point(start: PlanarPoint, end: PlanarPoint, fraction: float) -> PlanarPoint:
    return start[0] + (end[0] - start[0]) * fraction, start[1] + (end[1] - start[1]) * fraction


def _clamp_to_unit(value: float) -> float:
    return max(0.0, min(1.0, value))
