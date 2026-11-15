from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import orjson

from src.entities.gtfs import Route
from src.entities.gtfs import RoutePath
from src.models import polyline
from src.models.gtfs import StopTimeWithStopDetail
from src.models.polyline import RoutePathProjection
from src.repositories import route_path_repository


async def get_route_paths_by_route_short_name(route_short_name: str) -> List[RoutePath]:
    route_paths: List[RoutePath] = await route_path_repository.find_by_route_short_name(route_short_name)

    return route_paths


def select_route_path(route: Route, direction_id: Optional[int], route_paths: List[RoutePath]) -> Optional[RoutePath]:
    for route_path in route_paths:
        if route.route_code and route_path.route_code == route.route_code:
            return route_path

    candidates: List[RoutePath] = [route_path for route_path in route_paths if route_path.direction_id == direction_id]
    if not candidates:
        return None

    return min(
        candidates,
        key=lambda route_path: (route_path.departure_no != 0, -route_path.length_in_meters, route_path.route_code)
    )


def project_stops_onto_route_path(
        route_path: RoutePath,
        stop_times_with_stop_details: List[StopTimeWithStopDetail],
        route_path_projections_by_keys: Dict[Tuple, Optional[RoutePathProjection]]
) -> Optional[RoutePathProjection]:
    key = (route_path.route_path_id, tuple(stop_time.stop_id for stop_time in stop_times_with_stop_details))
    if key not in route_path_projections_by_keys:
        route_path_projections_by_keys[key] = polyline.project_stops_onto_route_path(
            [[stop_time.stop_lon, stop_time.stop_lat] for stop_time in stop_times_with_stop_details],
            orjson.loads(route_path.coordinates)
        )

    return route_path_projections_by_keys[key]
