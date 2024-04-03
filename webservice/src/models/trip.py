import itertools
import math
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Tuple
from decimal import Decimal, ROUND_HALF_EVEN

from loguru import logger

from src.entities.gtfs import Shape
from src.models.gtfs import StopTimeWithStopDetail


FivePlaces = Decimal('1e-5')


class TripGeometry:
    def __init__(
            self,
            *,
            trip_id: int,
            stop_times_with_stop_details: List[StopTimeWithStopDetail],
            shapes: List[Shape],
            properties: Dict
    ):
        self.trip_id: int = trip_id
        self.stop_times_with_stop_details: List[StopTimeWithStopDetail] = stop_times_with_stop_details
        self.properties: Dict = properties or {}
        self.shapes: List[Shape] = shapes
        self.coordinates: List[List] = []

    @property
    def stop_ids(self) -> List[int]:
        return [stop_time.stop_id for stop_time in self.stop_times_with_stop_details]

    def sort(self, strategy: str = 'arrival_time') -> None:
        self.stop_times_with_stop_details.sort(
            key=lambda stop_times_with_stop_detail: getattr(stop_times_with_stop_detail, strategy))

    def sort_by_stop_sequence(self) -> None:
        self.stop_times_with_stop_details.sort(key=lambda stop_time: stop_time.stop_sequence)

    def sort_by_arrival_time(self) -> None:
        self.stop_times_with_stop_details.sort(key=lambda stop_time: stop_time.arrival_time)

    def sort_by_departure_time(self) -> None:
        self.stop_times_with_stop_details.sort(key=lambda stop_time: stop_time.departure_time)

    def fill_geometry(self):
        self.sort_by_stop_sequence()
        self.estimate_arrival_times_by_haversine_interpolation()
        self.generate_line_string_geometry()

    def reset_first_departure_and_last_arrival_times_to_origin_date(self) -> None:
        first_departure_time: datetime = self.stop_times_with_stop_details[0].departure_time
        last_arrival_time: datetime = self.stop_times_with_stop_details[-1].arrival_time
        self.stop_times_with_stop_details[0].reset_departure_time_to_origin_date()
        self.stop_times_with_stop_details[0].reset_arrival_time_to_origin_date()
        is_last_arrival_time_in_next_day: bool = last_arrival_time.day != first_departure_time.day
        if is_last_arrival_time_in_next_day:
            self.stop_times_with_stop_details[-1].reset_arrival_time_to_origin_date(day=2)
        else:
            self.stop_times_with_stop_details[-1].reset_arrival_time_to_origin_date()

    def estimate_arrival_times_by_haversine_interpolation(self) -> None:
        total_haversine_distance: float = 0.0
        haversine_distance_between_stop_times_by_stop_id_pairs: Dict[Tuple, float] = {}
        self.reset_first_departure_and_last_arrival_times_to_origin_date()
        departure_time_at_first_stop: datetime = self.stop_times_with_stop_details[0].departure_time
        arrival_time_at_last_stop: datetime = self.stop_times_with_stop_details[-1].arrival_time
        total_time: timedelta = arrival_time_at_last_stop - departure_time_at_first_stop

        if total_time.days < 0:
            logger.warning(f"Total_time.days < 0: {total_time.days}")

        for left, right in itertools.pairwise(self.stop_times_with_stop_details):
            haversine_distance = self.haversine_distance_between(left, right)
            haversine_distance_between_stop_times_by_stop_id_pairs[(left.stop_id, right.stop_id)] = haversine_distance
            total_haversine_distance += haversine_distance

        for left, right in itertools.pairwise(self.stop_times_with_stop_details):
            haversine_distance = haversine_distance_between_stop_times_by_stop_id_pairs[(left.stop_id, right.stop_id)]
            time_delta = total_time * (haversine_distance / total_haversine_distance)
            estimated_arrival_time = left.departure_time.replace(
                year=left.departure_time.year,
                month=left.departure_time.month,
                day=left.departure_time.day) + time_delta
            estimated_arrival_time = estimated_arrival_time
            right.arrival_time = estimated_arrival_time - timedelta(seconds=30)
            right.departure_time = estimated_arrival_time

        logger.debug(f"Departure time at first stop: {departure_time_at_first_stop}")
        logger.debug(f"Arrival time at last stop: {arrival_time_at_last_stop}")
        logger.debug(f"Total trip time: {total_time}")

    def generate_line_string_geometry(self):
        self.coordinates.extend([
            [
                Decimal(stop_time.stop_lon).quantize(FivePlaces, rounding=ROUND_HALF_EVEN),
                Decimal(stop_time.stop_lat).quantize(FivePlaces, rounding=ROUND_HALF_EVEN),
                # stop_time.stop_lon,
                # stop_time.stop_lat,
                0,
                int(stop_time.arrival_time.timestamp())
            ]
            for stop_time
            in self.stop_times_with_stop_details
        ])

    @staticmethod
    def haversine_distance_between(left: StopTimeWithStopDetail, right: StopTimeWithStopDetail) -> float:
        # Radius of the Earth in kilometers
        radius_of_earth_in_kilometers = 6371.0

        lat1, lon1 = math.radians(left.stop_lat), math.radians(left.stop_lon)
        lat2, lon2 = math.radians(right.stop_lat), math.radians(right.stop_lon)

        distance_between_latitudes = lat2 - lat1
        distance_between_longitudes = lon2 - lon1

        a = math.sin(distance_between_latitudes / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(
            distance_between_longitudes / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = radius_of_earth_in_kilometers * c

        return distance
