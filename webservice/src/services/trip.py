from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from loguru import logger

from src.entities.gtfs import RoutePath
from src.entities.gtfs import Trip
from src.models.gtfs import StopTimeWithStopDetail
from src.models.polyline import RoutePathProjection
from src.models.trip import TripGeometry
from src.services import routepath as route_path_service
from src.services import stop as stop_service


def get_trip_geometry(
        trip: Trip,
        route_path: Optional[RoutePath],
        *,
        properties: Dict,
        route_path_projections_by_keys: Dict[Tuple, Optional[RoutePathProjection]]
) -> TripGeometry:
    stop_times_with_stop_details: List[StopTimeWithStopDetail] = sorted(
        [
            stop_service.map_stop_time_to_stop_time_with_stop_detail(stop_time)
            for stop_time
            in trip.stop_times
        ],
        key=lambda stop_time: stop_time.stop_sequence
    )
    route_path_projection: Optional[RoutePathProjection] = None
    if route_path:
        route_path_projection = route_path_service.project_stops_onto_route_path(
            route_path, stop_times_with_stop_details, route_path_projections_by_keys
        )
    if not route_path_projection:
        logger.debug(f"No route path projection for trip: {trip.trip_id}, falling back to stop chords")

    trip_geometry = TripGeometry(
        trip_id=trip.trip_id,
        stop_times_with_stop_details=stop_times_with_stop_details,
        properties=properties,
        route_path_projection=route_path_projection
    )
    with logger.contextualize(trip_id=trip.trip_id):
        trip_geometry.fill_geometry()

    return trip_geometry


"""
def get_feature_collection_by_trip(route_id: int, route_short_name: str, trip: Trip):
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "route_id": route_id,
                    "route_short_name": route_short_name,
                    "trip_id": trip.trip_id,
                    "trip_headsign": trip.trip_headsign,
                    "direction_id": trip.direction_id
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [stop_time.stop.stop_lon, stop_time.stop.stop_lat] for stop_time in trip.stop_times
                    ]
                }
            }
        ]
    }

    return feature_collection

"""
