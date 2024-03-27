from typing import Dict
from typing import List

from loguru import logger

from src.entities.gtfs import Route
from src.entities.gtfs import Trip
from src.models.trip import TripGeometry


class RoutesWithTripGeometries:
    def __init__(self, *, route_short_name: str, routes: List[Route]):
        self.route_short_name: str = route_short_name
        self.routes: List[Route] = routes
        #
        self.trip_geometries_by_trip_ids: Dict[int, TripGeometry] = {}

    @property
    def trips(self) -> List[Trip]:
        return [
            trip
            for route in self.routes
            for trip in route.trips
        ]

    @property
    def trip_geometries(self) -> List[TripGeometry]:
        if not self.trip_geometries_by_trip_ids:
            logger.warning(f"Trip Geometries not yet drawn!")

        return list(self.trip_geometries_by_trip_ids.values())
