from typing import List

from fastapi import APIRouter
from fastapi import Query
from fastapi.responses import ORJSONResponse
from loguru import logger

from src.docs.deck import GET_ROUTES_BY_ROUTE_SHORT_NAME_RESPONSE_EXAMPLE
from src.docs.deck import GET_ROUTE_TRIP_GEOMETRIES_BY_ROUTE_SHORT_NAME_RESPONSE_EXAMPLE
from src.entities.gtfs import Route
from src.mappers import deck as deck_mapper
from src.models.route import RoutesWithTripGeometries
from src.models.router.deck import GetRouteTripGeometriesByRouteShortNameResponse
from src.models.router.deck import GetRoutesByRouteShortNameResponse
from src.services import deck as deck_service

router = APIRouter(prefix='/deck', tags=['deck.gl'])


@router.get(
    path='/trip-geometries',
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": GET_ROUTE_TRIP_GEOMETRIES_BY_ROUTE_SHORT_NAME_RESPONSE_EXAMPLE
                }
            },
        },
    }
)
async def get_trip_geometries_by_route_short_name(
        route_short_name: str = Query(..., title="Route Short Name", alias='routeShortName', example='76Y')
) -> ORJSONResponse:
    with logger.contextualize(route_short_name=route_short_name):
        routes_with_trip_geometries: RoutesWithTripGeometries = await deck_service.get_trip_layer_geometries_by_route_short_name(
            route_short_name
        )
    get_route_trip_geometries_by_route_short_name_response: GetRouteTripGeometriesByRouteShortNameResponse = deck_mapper.map_routes_with_geometries_to_get_route_trip_geometries_by_route_short_name_response(
        routes_with_trip_geometries
    )

    return ORJSONResponse(
        content=get_route_trip_geometries_by_route_short_name_response.dict(by_alias=True).get('__root__', [])
    )


@router.get(
    path='/routes',
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": GET_ROUTES_BY_ROUTE_SHORT_NAME_RESPONSE_EXAMPLE
                }
            },
        },
    }
)
async def get_route_by_route_short_name(
        route_short_name: str = Query(..., title="Route Short Name", alias='routeShortName', example='76Y')
) -> ORJSONResponse:
    with logger.contextualize(route_short_name=route_short_name):
        routes: List[Route] = await deck_service.get_routes_by_route_short_name(route_short_name)
    get_routes_by_route_short_name_response: GetRoutesByRouteShortNameResponse = deck_mapper.map_routes_to_get_routes_by_route_short_name_response(
        routes
    )

    return ORJSONResponse(
        content=get_routes_by_route_short_name_response.dict(by_alias=True).get('__root__', [])
    )
