from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from loguru import logger

from src.entities.gtfs import Route
from src.entities.gtfs import RoutePath
from src.models.polyline import RoutePathProjection
from src.models.route import RoutesWithTripGeometries
from src.repositories import route_repository
from src.services import routepath as route_path_service
from src.services import trip as trip_service


async def get_route_by_id(route_id: int) -> Route:
    route: Route = await route_repository.find_by_id(route_id)

    return route


async def get_routes_by_route_short_name(route_short_name: str) -> List[Route]:
    routes: List[Route] = await route_repository.find_by_short_name(route_short_name)

    return routes


def draw_trip_geometries(
        route_short_name: str,
        routes: List[Route],
        route_paths: List[RoutePath]
) -> RoutesWithTripGeometries:
    routes_with_trip_geometries = RoutesWithTripGeometries(route_short_name=route_short_name, routes=routes)
    route_path_projections_by_keys: Dict[Tuple, Optional[RoutePathProjection]] = {}
    for route in routes_with_trip_geometries.routes:
        with logger.contextualize(route_id=route.route_id):
            for trip in route.trips:
                route_path: Optional[RoutePath] = route_path_service.select_route_path(route, trip.direction_id, route_paths)
                properties = {
                    'trip_id': trip.trip_id,
                    'route_id': route.route_id,
                    'route_short_name': route_short_name,
                    'route_path_id': route_path.route_path_id if route_path else None
                }
                routes_with_trip_geometries.trip_geometries_by_trip_ids[trip.trip_id] = trip_service.get_trip_geometry(
                    trip,
                    route_path,
                    properties=properties,
                    route_path_projections_by_keys=route_path_projections_by_keys
                )

    return routes_with_trip_geometries


async def get_routes_with_trip_geometries_by_route_short_name(route_short_name: str) -> RoutesWithTripGeometries:
    routes: List[Route] = await route_repository.find_by_short_name_with_trips_with_stop_times(route_short_name)
    route_paths: List[RoutePath] = await route_path_service.get_route_paths_by_route_short_name(route_short_name)
    logger.debug(f"Found {len(route_paths)} route paths!")
    routes_with_trip_geometries = draw_trip_geometries(route_short_name, routes, route_paths)

    return routes_with_trip_geometries
