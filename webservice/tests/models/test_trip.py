from datetime import datetime
from datetime import timezone
from typing import List

import pytest

from src.models import polyline
from src.models.gtfs import StopTimeWithStopDetail
from src.models.trip import TripGeometry

STRAIGHT_PATH = [[29.00, 41.0], [29.01, 41.0], [29.02, 41.0], [29.03, 41.0]]
DEPARTURE = datetime(2026, 11, 15, 6, 40, tzinfo=timezone.utc)
ARRIVAL = datetime(2026, 11, 15, 7, 10, tzinfo=timezone.utc)
ORIGIN_DEPARTURE_TIMESTAMP = int(datetime(1970, 1, 1, 6, 40, tzinfo=timezone.utc).timestamp())
ORIGIN_ARRIVAL_TIMESTAMP = int(datetime(1970, 1, 1, 7, 10, tzinfo=timezone.utc).timestamp())


def _stop_time(stop_id: int, stop_sequence: int, lon: float, lat: float, time=None) -> StopTimeWithStopDetail:
    return StopTimeWithStopDetail(
        stop_id=stop_id,
        stop_code=stop_id,
        stop_name=f'stop {stop_id}',
        stop_desc='',
        stop_lat=lat,
        stop_lon=lon,
        location_type=0,
        stop_sequence=stop_sequence,
        arrival_time=time,
        departure_time=time,
        timepoint=1 if time else 0
    )


def _stop_times() -> List[StopTimeWithStopDetail]:
    return [
        _stop_time(3, 3, 29.025, 41.0001, ARRIVAL),
        _stop_time(1, 1, 29.005, 41.0001, DEPARTURE),
        _stop_time(2, 2, 29.015, 40.9999),
    ]


class TestFillGeometry:
    def test_given_route_path_projection_when_filled_then_coordinates_follow_route_path(self):
        stop_times = sorted(_stop_times(), key=lambda stop_time: stop_time.stop_sequence)
        projection = polyline.project_stops_onto_route_path(
            [[stop_time.stop_lon, stop_time.stop_lat] for stop_time in stop_times], STRAIGHT_PATH
        )
        trip_geometry = TripGeometry(trip_id=1, stop_times_with_stop_details=_stop_times(), properties={}, route_path_projection=projection)

        trip_geometry.fill_geometry()

        coordinates = [[float(coordinate[0]), float(coordinate[1])] for coordinate in trip_geometry.coordinates]
        assert coordinates == [[29.005, 41.0], [29.01, 41.0], [29.02, 41.0], [29.025, 41.0]]

    def test_given_route_path_projection_when_filled_then_timestamps_span_departure_to_arrival(self):
        stop_times = sorted(_stop_times(), key=lambda stop_time: stop_time.stop_sequence)
        projection = polyline.project_stops_onto_route_path(
            [[stop_time.stop_lon, stop_time.stop_lat] for stop_time in stop_times], STRAIGHT_PATH
        )
        trip_geometry = TripGeometry(trip_id=1, stop_times_with_stop_details=_stop_times(), properties={}, route_path_projection=projection)

        trip_geometry.fill_geometry()

        timestamps = [coordinate[3] for coordinate in trip_geometry.coordinates]
        assert timestamps[0] == ORIGIN_DEPARTURE_TIMESTAMP
        assert timestamps[-1] == ORIGIN_ARRIVAL_TIMESTAMP
        assert timestamps == sorted(timestamps)
        assert timestamps[1] - timestamps[0] == pytest.approx(450, abs=2)

    def test_given_no_route_path_projection_when_filled_then_falls_back_to_stop_chords(self):
        trip_geometry = TripGeometry(trip_id=1, stop_times_with_stop_details=_stop_times(), properties={})

        trip_geometry.fill_geometry()

        coordinates = [[float(coordinate[0]), float(coordinate[1])] for coordinate in trip_geometry.coordinates]
        assert coordinates == [[29.005, 41.0001], [29.015, 40.9999], [29.025, 41.0001]]
        assert trip_geometry.coordinates[0][3] == ORIGIN_DEPARTURE_TIMESTAMP
