from collections import defaultdict
from typing import Dict
from typing import List

from loguru import logger

from src.entities.gtfs import Route
from src.entities.gtfs import Shape
from src.models.route import RoutesWithTripGeometries
from src.repositories import route_repository
from src.services import trip as trip_service
from src.services import shape as shape_service


async def get_route_by_id(route_id: int) -> Route:
    route: Route = await route_repository.find_by_id(route_id)

    return route


async def get_routes_by_route_short_name(route_short_name: str) -> List[Route]:
    routes: List[Route] = await route_repository.find_by_short_name(route_short_name)

    return routes


def draw_trip_geometries(
        route_short_name: str,
        routes: List[Route],
        shapes_by_shape_ids: Dict[int, List[Shape]]
) -> RoutesWithTripGeometries:
    routes_with_trip_geometries = RoutesWithTripGeometries(route_short_name=route_short_name, routes=routes)
    for route in routes_with_trip_geometries.routes:
        with logger.contextualize(route_id=route.route_id):
            for trip in route.trips:
                properties = {
                    'trip_id': trip.trip_id,
                    'route_id': route.route_id,
                    'route_short_name': route_short_name
                }
                routes_with_trip_geometries.trip_geometries_by_trip_ids[trip.trip_id] = trip_service.get_trip_geometry(
                    trip,
                    shapes_by_shape_ids.get(trip.shape_id, []),
                    properties=properties
                )

    return routes_with_trip_geometries


def find_unique_shape_ids(routes: List[Route]) -> List[int]:
    shape_ids = set()
    for route in routes:
        for trip in route.trips:
            if trip.shape_id:
                shape_ids.add(trip.shape_id)

    return list(shape_ids)


def hash_shape_sequences_by_shape_ids(shapes: List[Shape]) -> Dict[int, List[Shape]]:
    shape_records_by_shape_ids = defaultdict(list)
    for shape in shapes:
        shape_records_by_shape_ids[shape.shape_id].append(shape)

    for shape_id, shape_records in shape_records_by_shape_ids.items():
        shape_records_by_shape_ids[shape_id] = sorted(shape_records, key=lambda s: s.shape_pt_sequence)
        logger.debug(f"Shape {shape_id} has {len(shape_records_by_shape_ids[shape_id])} points in sequence!")

    return shape_records_by_shape_ids


async def get_routes_with_trip_geometries_by_route_short_name(route_short_name: str) -> RoutesWithTripGeometries:
    routes: List[Route] = await route_repository.find_by_short_name_with_trips_with_stop_times(route_short_name)
    unique_shape_ids: List[int] = find_unique_shape_ids(routes)
    logger.debug(f"Found {len(unique_shape_ids)} unique shape ids!")
    logger.debug(f"Shape ids: {unique_shape_ids}")
    shapes: List[Shape] = await shape_service.get_shapes_by_ids(unique_shape_ids)
    shape_sequences_by_shape_ids: Dict[int, List[Shape]] = hash_shape_sequences_by_shape_ids(shapes)
    routes_with_trip_geometries = draw_trip_geometries(route_short_name, routes, shape_sequences_by_shape_ids)

    return routes_with_trip_geometries
