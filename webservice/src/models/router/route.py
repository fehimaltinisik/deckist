from typing import Dict
from typing import List

from tortoise.contrib.pydantic import pydantic_model_creator

from src.config.dto import DataTransferObject
from src.config.dto import DataTransferObjectConfig
from src.entities.gtfs import Route
from src.models.router.deck import RoutesByRouteShortNameWithTripsWithStopTimesResponse


RouteResponse = pydantic_model_creator(
    cls=Route,
    name='RouteResponse',
    config_class=DataTransferObjectConfig,
    exclude=('trips',)
)
GetRouteByIdResponse = RouteResponse
GetRoutesByRouteShortNameResponse = List[RouteResponse]
GetRoutesByRouteShortNameWithTripsWithStopTimesResponse = List[RoutesByRouteShortNameWithTripsWithStopTimesResponse]


class GetRouteGeometriesByRouteShortNameResponse(DataTransferObject):
    class TripGeometry(DataTransferObject):
        trip_id: int
        properties: Dict[str, str]
        coordinates: List[List[float]]

    route_short_name: str
    trip_geometries: List[TripGeometry]
