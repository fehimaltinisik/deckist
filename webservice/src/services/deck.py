from itertools import groupby
from typing import Dict
from typing import List
from typing import Optional

from loguru import logger

from src.entities.gtfs import Route
from src.models.deck import DeckGLRoutesWithTripGeometries
from src.models.dto.s3 import DeckGLRouteTripGeometriesByRouteShortNameObject
from src.models.route import RoutesWithTripGeometries
from src.models.router.deck import GetDeckGLRouteTripGeometriesByRouteShortNameResponse
from src.models.trip import TripGeometry
from src.services import route as route_service
from src.mappers import deck as deck_mapper
from src.services import s3 as s3service


def minimize_trip_geometries(routes_with_trip_geometries: RoutesWithTripGeometries) -> DeckGLRoutesWithTripGeometries:
    trip_ids_by_path_ids: Dict[int, List[int]] = {}
    path_coordinates_by_path_ids: Dict[int, List[List[float]]] = {}
    path_timestamp_difference_by_path_ids: Dict[int, List[int]] = {}
    trip_timestamps_by_trip_ids: Dict[int, List] = {}
    for trip_id, trip_geometry in routes_with_trip_geometries.trip_geometries_by_trip_ids.items():
        trip_timestamps_by_trip_ids[trip_id] = [coordinate[3] for coordinate in trip_geometry.coordinates]

    for path_id, (stop_ids, trip_geometries_grouper) in enumerate(groupby(routes_with_trip_geometries.trip_geometries, key=lambda tg: str(tg.stop_ids))):
        trip_geometries: List[TripGeometry] = list(trip_geometries_grouper)
        trip_ids: List[int] = [trip_geometry.trip_id for trip_geometry in trip_geometries]
        trip_ids_by_path_ids[path_id] = trip_ids
        first_trip_geometries_coordinates = list(trip_geometries)[0].coordinates
        trip_departures_timestamp = first_trip_geometries_coordinates[0][3]
        timestamp_difference: List[int] = [coordinate[3] - trip_departures_timestamp for coordinate in first_trip_geometries_coordinates]
        path_coordinates_by_path_ids[path_id] = [[coordinate[0], coordinate[1]] for coordinate in first_trip_geometries_coordinates]
        path_timestamp_difference_by_path_ids[path_id] = timestamp_difference

    return DeckGLRoutesWithTripGeometries(
        route_short_name=routes_with_trip_geometries.route_short_name,
        routes=routes_with_trip_geometries.routes,
        trip_geometries_by_trip_ids=routes_with_trip_geometries.trip_geometries_by_trip_ids,
        trip_timestamps_by_trip_ids=trip_timestamps_by_trip_ids,
        trip_ids_by_path_ids=trip_ids_by_path_ids,
        path_coordinates_by_path_ids=path_coordinates_by_path_ids,
        path_timestamp_difference_by_path_ids=path_timestamp_difference_by_path_ids
    )


async def get_trip_geometries_by_route_short_name(route_short_name: str) -> RoutesWithTripGeometries:
    routes_with_trip_geometries: RoutesWithTripGeometries = await route_service.get_routes_with_trip_geometries_by_route_short_name(
        route_short_name
    )

    return routes_with_trip_geometries


async def get_compact_trip_geometries_by_route_short_name(route_short_name: str) -> GetDeckGLRouteTripGeometriesByRouteShortNameResponse:
    deck_gl_route_trip_geometries_by_route_short_name_s3_object: Optional[DeckGLRouteTripGeometriesByRouteShortNameObject] = s3service.download_routes_with_trip_geometries_from_s3_as_route_segments_file_object(
        route_short_name
    )
    if deck_gl_route_trip_geometries_by_route_short_name_s3_object:
        logger.info("Route Geometries already exists in S3")
        return deck_mapper.map_deck_gl_route_trip_geometries_by_route_short_name_object_to_get_routes_with_trip_geometries_by_route_short_name(
            deck_gl_route_trip_geometries_by_route_short_name_s3_object
        )

    logger.info("Route Geometries does not exist in S3. Generating Route Geometries")
    routes_with_trip_geometries: RoutesWithTripGeometries = await route_service.get_routes_with_trip_geometries_by_route_short_name(
        route_short_name
    )
    deck_routes_with_trip_geometries: DeckGLRoutesWithTripGeometries = minimize_trip_geometries(routes_with_trip_geometries)
    get_compact_trip_geometries_by_route_short_name_response: GetDeckGLRouteTripGeometriesByRouteShortNameResponse = deck_mapper.map_routes_with_geometries_to_get_compact_trip_geometries_by_route_short_name_response(
        deck_routes_with_trip_geometries
    )

    return get_compact_trip_geometries_by_route_short_name_response


async def upload_route_coordinates_by_route_short_name_to_s3(route_short_name: str):
    routes_with_trip_geometries: RoutesWithTripGeometries = await route_service.get_routes_with_trip_geometries_by_route_short_name(
        route_short_name
    )
    deck_routes_with_trip_geometries: DeckGLRoutesWithTripGeometries = minimize_trip_geometries(routes_with_trip_geometries)
    s3service.upload_routes_with_trip_geometries_to_s3_as_route_segments_file_object(
        route_short_name=route_short_name, deck_gl_routes_with_trip_geometries=deck_routes_with_trip_geometries
    )


async def get_routes_by_route_short_name(route_short_name: str) -> List[Route]:
    routes: List[Route] = await route_service.get_routes_by_route_short_name(
        route_short_name)

    return routes
