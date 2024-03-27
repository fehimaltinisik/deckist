from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel

from src.config.dto import DataTransferObject
from src.config.dto import DataTransferObjectConfig

"""
class FeatureCollection(BaseModel):
    type: str = 'FeatureCollection'
    features: List['Feature']

    class Feature(BaseModel):
        type: str = 'Feature'
        properties: Dict
        geometry: 'GetRouteByIdResponse.Geometry'
        id: str

        class Geometry(BaseModel):
            type: str = 'LineString'
            coordinates: List[List[float]]
"""


class RoutesByRouteShortNameWithTripsWithStopTimesResponse(BaseModel):
    route_id: int
    route_short_name: str
    route_long_name: str
    route_code: str
    trips: List['Trip']

    class Trip(BaseModel):
        trip_id: int
        service_id: int
        trip_headsign: str
        direction_id: int
        stop_times: List['StopTimeWithStopDetails']

        class StopTimeWithStopDetails(BaseModel):
            stop_id: int
            stop_code: str
            stop_name: str
            stop_desc: str
            stop_lat: float
            stop_lon: float
            location_type: int
            stop_sequence: int
            arrival_time: Optional[datetime]
            departure_time: Optional[datetime]
            timepoint: int


class Geometry(DataTransferObject):
    type: str = 'LineString'
    coordinates: List[List[float]] = []


class Feature(DataTransferObject):
    type: str = 'Feature'
    geometry: Geometry
    properties: Dict


class FeatureCollection(DataTransferObject):
    type: str = 'FeatureCollection'
    features: List[Feature] = []


class Segment(DataTransferObject):
    route_short_name: str
    trip_id: int
    route_id: int
    path: List[List[float]] = []
    timestamps: List[int] = []

    class Config(DataTransferObjectConfig):
        pass


class GetRouteTripGeometriesByRouteShortNameResponse(BaseModel):
    __root__: List[Segment]


class GetRoutesByRouteShortNameResponse(DataTransferObject):
    class Route(DataTransferObject):
        route_id: int
        route_short_name: str

    __root__: List[Route]
