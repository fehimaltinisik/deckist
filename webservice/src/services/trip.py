from typing import Dict
from typing import List

from loguru import logger

from src.entities.gtfs import Shape
from src.entities.gtfs import Trip
from src.models.gtfs import StopTimeWithStopDetail
from src.models.trip import TripGeometry
from src.services import stop as stop_service


def get_trip_geometry(trip: Trip, shapes: List[Shape], *, properties: Dict) -> TripGeometry:
    if not shapes:
        logger.debug(f"No shapes found for trip: {trip.trip_id}")

    stop_times_with_stop_details: List[StopTimeWithStopDetail] = [
        stop_service.map_stop_time_to_stop_time_with_stop_detail(stop_time)
        for stop_time
        in trip.stop_times
    ]
    trip_geometry = TripGeometry(
        trip_id=trip.trip_id,
        stop_times_with_stop_details=stop_times_with_stop_details,
        shapes=shapes,
        properties=properties
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
