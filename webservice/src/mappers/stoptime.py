from typing import List

from src.entities.gtfs import StopTime
from src.models.gtfs import StopTimeWithStopDetail


def map_stop_time_to_stop_time_with_stop_detail(stop_time: StopTime) -> StopTimeWithStopDetail:
    return StopTimeWithStopDetail(
        stop_id=stop_time.stop.stop_id,
        stop_code=stop_time.stop.stop_code,
        stop_name=stop_time.stop.stop_name,
        stop_desc=stop_time.stop.stop_desc,
        stop_lat=stop_time.stop.stop_lat,
        stop_lon=stop_time.stop.stop_lon,
        location_type=stop_time.stop.location_type,
        stop_sequence=stop_time.stop_sequence,
        arrival_time=stop_time.arrival_time,
        departure_time=stop_time.departure_time,
        timepoint=stop_time.timepoint
    )
