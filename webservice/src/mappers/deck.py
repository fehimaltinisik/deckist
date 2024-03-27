from typing import List

from src.entities.gtfs import Route
from src.models.route import RoutesWithTripGeometries
from src.models.router.deck import GetRouteTripGeometriesByRouteShortNameResponse
from src.models.router.deck import GetRoutesByRouteShortNameResponse


def map_routes_with_geometries_to_get_route_trip_geometries_by_route_short_name_response(
        route_with_trip_geometries: RoutesWithTripGeometries) -> GetRouteTripGeometriesByRouteShortNameResponse:
    route_segments = []
    for trip_geometry in route_with_trip_geometries.trip_geometries:
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


def map_routes_to_get_routes_by_route_short_name_response(routes: List[Route]) -> GetRoutesByRouteShortNameResponse:
    return GetRoutesByRouteShortNameResponse.parse_obj(routes)
