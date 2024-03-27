from typing import List

from src.entities.gtfs import Route
from src.models.route import RoutesWithTripGeometries
from src.models.router.route import GetRouteByIdResponse
from src.models.router.route import GetRouteGeometriesByRouteShortNameResponse
from src.models.router.route import GetRoutesByRouteShortNameResponse
from src.models.router.route import RouteResponse


def map_route_to_get_route_by_id_response(route: Route) -> GetRouteByIdResponse:
    return GetRouteByIdResponse.from_orm(route)


def map_routes_to_get_routes_by_route_short_name_response(routes: List[Route]) -> GetRoutesByRouteShortNameResponse:
    return [RouteResponse.from_orm(route) for route in routes]


def map_routes_with_trip_geometries_to_get_route_geometries_by_route_short_name_response(
        routes_with_trip_geometries: RoutesWithTripGeometries
) -> GetRouteGeometriesByRouteShortNameResponse:
    return GetRouteGeometriesByRouteShortNameResponse.from_orm(routes_with_trip_geometries)
