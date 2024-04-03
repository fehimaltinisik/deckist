from typing import Dict
from typing import List

from src.entities.gtfs import Route
from src.models.trip import TripGeometry


class DeckGLRoutesWithTripGeometries:
    def __init__(
            self,
            *,
            route_short_name: str,
            routes: List[Route],
            trip_geometries_by_trip_ids: Dict[int, TripGeometry],
            trip_ids_by_path_ids: Dict[int, List[int]],
            path_coordinates_by_path_ids: Dict[int, List[List[float]]],
            path_timestamp_difference_by_path_ids: Dict[int, List[int]],
            trip_timestamps_by_trip_ids: Dict[int, List[int]],

    ):
        self.route_short_name: str = route_short_name
        self.routes: List[Route] = routes
        #
        self.trip_geometries_by_trip_ids: Dict[int, TripGeometry] = trip_geometries_by_trip_ids
        self.trip_ids_by_path_ids: Dict[int, List[int]] = trip_ids_by_path_ids
        self.path_coordinates_by_path_ids: Dict[int, List[List[float]]] = path_coordinates_by_path_ids
        self.path_timestamp_difference_by_path_ids: Dict[int, List[int]] = path_timestamp_difference_by_path_ids
        self.trip_timestamps_by_trip_ids: Dict[int, List[int]] = trip_timestamps_by_trip_ids
