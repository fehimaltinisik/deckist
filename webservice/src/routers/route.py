from typing import List

from fastapi import APIRouter
from fastapi import Path
from fastapi import Query
from fastapi.responses import ORJSONResponse
from loguru import logger

from src.docs.route import GET_ROUTE_GEOMETRIES_BY_ROUTE_SHORT_NAME_RESPONSE_EXAMPLE
from src.entities.gtfs import Route
from src.mappers import route_mapper
from src.models.route import RoutesWithTripGeometries
from src.models.router.route import GetRouteByIdResponse
from src.models.router.route import GetRouteGeometriesByRouteShortNameResponse
from src.models.router.route import GetRoutesByRouteShortNameResponse
from src.services import route as route_service
from starlette.status import HTTP_200_OK


route_router = APIRouter(prefix='/route', tags=['route'])
routes_router = APIRouter(prefix='/routes', tags=['routes'])


@route_router.get('/{route_id}')
async def get_route_by_id(
        route_id: int = Path(..., title="Route ID", alias='route_id', min=1, example=3188)
) -> GetRouteByIdResponse:
    route: Route = await route_service.get_route_by_id(route_id)
    get_route_by_id_response: GetRouteByIdResponse = route_mapper.map_route_to_get_route_by_id_response(route)

    return get_route_by_id_response


@routes_router.get('/')
async def get_routes_by_route_short_name(
        route_short_name: str = Query(None, title="Route Short Name", alias='routeShortName', example='76Y')
) -> GetRoutesByRouteShortNameResponse:
    routes: List[Route] = await route_service.get_routes_by_route_short_name(route_short_name)
    get_routes_by_route_shot_name_response: GetRoutesByRouteShortNameResponse = route_mapper.map_routes_to_get_routes_by_route_short_name_response(
        routes)

    return get_routes_by_route_shot_name_response


@routes_router.get(
    path='/geometries',
    responses={
        HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": GET_ROUTE_GEOMETRIES_BY_ROUTE_SHORT_NAME_RESPONSE_EXAMPLE
                }
            },
        },
    }
)
async def get_route_geometries_by_route_short_name(
        route_short_name: str = Query(..., title="Route Short Name", alias='routeShortName', example='76Y')
) -> ORJSONResponse:
    with logger.contextualize(route_short_name=route_short_name):
        routes_with_trip_geometries: RoutesWithTripGeometries = await route_service.get_routes_with_trip_geometries_by_route_short_name(
            route_short_name)

    get_route_geometries_by_route_short_name_response: GetRouteGeometriesByRouteShortNameResponse = route_mapper.map_routes_with_trip_geometries_to_get_route_geometries_by_route_short_name_response(
        routes_with_trip_geometries)

    return ORJSONResponse(content=get_route_geometries_by_route_short_name_response.dict(by_alias=True))
