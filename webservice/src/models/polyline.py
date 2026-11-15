import math
from functools import cached_property
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

EARTH_RADIUS_IN_METERS: float = 6371000.0
DEFAULT_MAX_STOP_OFFSET_IN_METERS: float = 200.0
DEFAULT_LOOKAHEAD_IN_METERS: float = 1500.0
DEFAULT_MAX_OUTLIER_STOP_RATIO: float = 0.1

Coordinate = Sequence[float]


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

    @cached_property
    def progress_vertices(self) -> List[Tuple[List[float], float]]:
        start, length = self.start_distance, self.end_distance - self.start_distance

        return [(coordinate, (distance - start) / length) for coordinate, distance in self.trim()]

    def trim(self) -> List[Tuple[List[float], float]]:
        start, end = self.start_distance, self.end_distance
        vertices: List[Tuple[List[float], float]] = [(interpolate_coordinate(self.coordinates, self.cumulative_distances, start), start)]
        for coordinate, distance in zip(self.coordinates, self.cumulative_distances):
            if start < distance < end:
                vertices.append((list(coordinate), distance))
        vertices.append((interpolate_coordinate(self.coordinates, self.cumulative_distances, end), end))

        return vertices


def project_stops_onto_route_path(
        stop_coordinates: Sequence[Coordinate],
        route_path_coordinates: Sequence[Coordinate],
        *,
        max_stop_offset_in_meters: float = DEFAULT_MAX_STOP_OFFSET_IN_METERS,
        lookahead_in_meters: float = DEFAULT_LOOKAHEAD_IN_METERS,
        max_outlier_stop_ratio: float = DEFAULT_MAX_OUTLIER_STOP_RATIO
) -> Optional[RoutePathProjection]:
    if len(stop_coordinates) < 2 or len(route_path_coordinates) < 2:
        return None

    reference_latitude: float = route_path_coordinates[0][1]
    path_points: List[Tuple[float, float]] = [_to_planar(coordinate, reference_latitude) for coordinate in route_path_coordinates]
    cumulative_distances: List[float] = _cumulative_distances(path_points)

    stop_distances: List[float] = []
    segment_index: int = 0
    previous_distance: float = 0.0
    outlier_stops: int = 0
    last_stop_index: int = len(stop_coordinates) - 1
    for stop_index, stop_coordinate in enumerate(stop_coordinates):
        stop_point = _to_planar(stop_coordinate, reference_latitude)
        projection = _find_nearest_segment_ahead(
            stop_point, path_points, cumulative_distances, segment_index, previous_distance,
            lookahead_in_meters, max_stop_offset_in_meters
        )
        if projection is None:
            return None

        is_outlier = projection[2] > max_stop_offset_in_meters
        is_end_stop = stop_index in (0, last_stop_index)
        if is_outlier and is_end_stop:
            return None

        if is_outlier:
            outlier_stops += 1
            stop_distances.append(previous_distance)
            continue

        segment_index, distance, _ = projection
        stop_distances.append(distance)
        previous_distance = distance

    if outlier_stops > max_outlier_stop_ratio * len(stop_coordinates):
        return None

    if stop_distances[-1] <= stop_distances[0]:
        return None

    return RoutePathProjection(
        coordinates=[list(coordinate[:2]) for coordinate in route_path_coordinates],
        cumulative_distances=cumulative_distances,
        stop_distances=stop_distances
    )


def interpolate_coordinate(coordinates: Sequence[Coordinate], cumulative_distances: Sequence[float], distance: float) -> List[float]:
    for index in range(1, len(cumulative_distances)):
        if cumulative_distances[index] >= distance:
            segment_length = cumulative_distances[index] - cumulative_distances[index - 1]
            fraction = 0.0 if segment_length == 0 else (distance - cumulative_distances[index - 1]) / segment_length
            left, right = coordinates[index - 1], coordinates[index]
            return [left[0] + (right[0] - left[0]) * fraction, left[1] + (right[1] - left[1]) * fraction]

    return list(coordinates[-1][:2])


def _find_nearest_segment_ahead(
        point: Tuple[float, float],
        path_points: List[Tuple[float, float]],
        cumulative_distances: List[float],
        start_segment_index: int,
        min_distance: float,
        lookahead_in_meters: float,
        max_stop_offset_in_meters: float
) -> Optional[Tuple[int, float, float]]:
    best: Optional[Tuple[int, float, float]] = None
    for index in range(start_segment_index, len(path_points) - 1):
        is_close_match_found = best is not None and best[2] <= max_stop_offset_in_meters
        if is_close_match_found and cumulative_distances[index] - best[1] > lookahead_in_meters:
            break

        fraction, offset = _project_onto_segment(point, path_points[index], path_points[index + 1])
        segment_length = cumulative_distances[index + 1] - cumulative_distances[index]
        distance = max(cumulative_distances[index] + fraction * segment_length, min_distance)
        if best is None or offset < best[2]:
            best = (index, distance, offset)

    return best


def _project_onto_segment(point, start, end) -> Tuple[float, float]:
    dx, dy = end[0] - start[0], end[1] - start[1]
    length_squared = dx * dx + dy * dy
    fraction = 0.0
    if length_squared > 0:
        fraction = max(0.0, min(1.0, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared))
    nearest_x, nearest_y = start[0] + fraction * dx, start[1] + fraction * dy

    return fraction, math.hypot(point[0] - nearest_x, point[1] - nearest_y)


def _cumulative_distances(points: List[Tuple[float, float]]) -> List[float]:
    distances: List[float] = [0.0]
    for left, right in zip(points, points[1:]):
        distances.append(distances[-1] + math.hypot(right[0] - left[0], right[1] - left[1]))

    return distances


def _to_planar(coordinate: Coordinate, reference_latitude: float) -> Tuple[float, float]:
    meters_per_degree = math.radians(1) * EARTH_RADIUS_IN_METERS

    return (
        coordinate[0] * meters_per_degree * math.cos(math.radians(reference_latitude)),
        coordinate[1] * meters_per_degree
    )
