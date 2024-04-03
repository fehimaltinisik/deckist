from typing import Dict
from typing import List

from src.config.dto import DataTransferObject


class DeckRouteSegment(DataTransferObject):
    route_short_name: str
    trip_id: int
    route_id: int
    path: List[List[float]] = []
    timestamps: List[int] = []


class DeckRouteSegments(DataTransferObject):
    __root__: List[DeckRouteSegment]


class DeckGLRouteTripGeometriesByRouteShortNameObject(DataTransferObject):
    class TripDetails(DataTransferObject):
        trip_id: int
        route_id: int
        departure_time: int

    route_short_name: str
    trip_ids_by_path_ids: Dict[int, List[int]]
    path_coordinates_by_path_ids: Dict[int, List[List[float]]]
    path_timestamp_difference_by_path_ids: Dict[int, List[int]]
    trip_details_by_trip_ids: Dict[int, TripDetails]
