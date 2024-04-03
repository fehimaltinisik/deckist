from typing import Dict
from typing import List

from src.entities.gtfs import Route
from src.models.deck import DeckGLRoutesWithTripGeometries
from src.models.dto.s3 import DeckGLRouteTripGeometriesByRouteShortNameObject
from src.models.route import RoutesWithTripGeometries
from src.models.router.deck import GetDeckGLRouteTripGeometriesByRouteShortNameResponse
from src.models.router.deck import GetRouteTripGeometriesByRouteShortNameResponse
from src.models.router.deck import GetRoutesByRouteShortNameResponse


def map_routes_with_geometries_to_get_route_trip_geometries_by_route_short_name_response(
        routes_with_trip_geometries: RoutesWithTripGeometries
) -> GetRouteTripGeometriesByRouteShortNameResponse:
    route_segments = []
    for trip_geometry in routes_with_trip_geometries.trip_geometries:
        coordinates = [[coordinate[0], coordinate[1]] for coordinate in trip_geometry.coordinates]
        timestamps = [coordinate[3] for coordinate in trip_geometry.coordinates]
        route_segments.append(
            {
                'trip_id': trip_geometry.properties['trip_id'],
                'route_id': trip_geometry.properties['route_id'],
                'route_short_name': trip_geometry.properties['route_short_name'],
                'path': coordinates,
                'timestamps': timestamps
            }
        )

    return GetRouteTripGeometriesByRouteShortNameResponse.parse_obj(route_segments)


def map_routes_with_geometries_to_get_compact_trip_geometries_by_route_short_name_response(
        deck_gl_routes_with_trip_geometries: DeckGLRoutesWithTripGeometries
) -> GetDeckGLRouteTripGeometriesByRouteShortNameResponse:
    trip_details_by_trip_ids: Dict[int, GetDeckGLRouteTripGeometriesByRouteShortNameResponse.TripDetails] = {}
    for trip_id, trip_geometry in deck_gl_routes_with_trip_geometries.trip_geometries_by_trip_ids.items():
        trip_details_by_trip_ids[trip_id] = GetDeckGLRouteTripGeometriesByRouteShortNameResponse.TripDetails(
            trip_id=trip_id,
            route_id=trip_geometry.properties['route_id'],
            departure_time=trip_geometry.coordinates[0][3]
        )

    return GetDeckGLRouteTripGeometriesByRouteShortNameResponse(
        route_short_name=deck_gl_routes_with_trip_geometries.route_short_name,
        trip_ids_by_path_ids=deck_gl_routes_with_trip_geometries.trip_ids_by_path_ids,
        path_coordinates_by_path_ids=deck_gl_routes_with_trip_geometries.path_coordinates_by_path_ids,
        path_timestamp_difference_by_path_ids=deck_gl_routes_with_trip_geometries.path_timestamp_difference_by_path_ids,
        trip_details_by_trip_ids=trip_details_by_trip_ids
    )


def map_routes_to_get_routes_by_route_short_name_response(routes: List[Route]) -> GetRoutesByRouteShortNameResponse:
    return GetRoutesByRouteShortNameResponse.parse_obj(routes)


def map_deck_gl_route_trip_geometries_by_route_short_name_object_to_deck_gl_routes_with_trip_geometries(
        deck_gl_route_trip_geometries_by_route_short_name_s3_object: DeckGLRouteTripGeometriesByRouteShortNameObject
) -> DeckGLRoutesWithTripGeometries:
    return DeckGLRoutesWithTripGeometries(
        route_short_name=deck_gl_route_trip_geometries_by_route_short_name_s3_object.route_short_name,
        routes=[],
        trip_geometries_by_trip_ids={},
        trip_ids_by_path_ids=deck_gl_route_trip_geometries_by_route_short_name_s3_object.trip_ids_by_path_ids,
        path_coordinates_by_path_ids=deck_gl_route_trip_geometries_by_route_short_name_s3_object.path_coordinates_by_path_ids,
        path_timestamp_difference_by_path_ids=deck_gl_route_trip_geometries_by_route_short_name_s3_object.path_timestamp_difference_by_path_ids,
        trip_timestamps_by_trip_ids={}
    )


def map_deck_gl_route_trip_geometries_by_route_short_name_object_to_get_routes_with_trip_geometries_by_route_short_name(
        deck_gl_route_trip_geometries_by_route_short_name_s3_object: DeckGLRouteTripGeometriesByRouteShortNameObject
) -> GetDeckGLRouteTripGeometriesByRouteShortNameResponse:
    return GetDeckGLRouteTripGeometriesByRouteShortNameResponse(
        route_short_name=deck_gl_route_trip_geometries_by_route_short_name_s3_object.route_short_name,
        trip_ids_by_path_ids=deck_gl_route_trip_geometries_by_route_short_name_s3_object.trip_ids_by_path_ids,
        path_coordinates_by_path_ids=deck_gl_route_trip_geometries_by_route_short_name_s3_object.path_coordinates_by_path_ids,
        path_timestamp_difference_by_path_ids=deck_gl_route_trip_geometries_by_route_short_name_s3_object.path_timestamp_difference_by_path_ids,
        trip_details_by_trip_ids={
            trip_id: GetDeckGLRouteTripGeometriesByRouteShortNameResponse.TripDetails(
                trip_id=trip_id,
                route_id=trip_details.route_id,
                departure_time=trip_details.departure_time
            ) for trip_id, trip_details in deck_gl_route_trip_geometries_by_route_short_name_s3_object.trip_details_by_trip_ids.items()
        }
    )
