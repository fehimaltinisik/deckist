from src.entities.gtfs import StopTime
from src.mappers import stoptime as stop_time_mapper
from src.models.gtfs import StopTimeWithStopDetail


def map_stop_time_to_stop_time_with_stop_detail(stop_time: StopTime) -> StopTimeWithStopDetail:
    return stop_time_mapper.map_stop_time_to_stop_time_with_stop_detail(stop_time)
