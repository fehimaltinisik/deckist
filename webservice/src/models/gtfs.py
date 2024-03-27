from datetime import datetime


class StopTimeWithStopDetail:
    def __init__(
            self,
            *,
            stop_id: int,
            stop_code: int,
            stop_name: str,
            stop_desc: str,
            stop_lat: float,
            stop_lon: float,
            location_type: int,
            # trip_id: int
            stop_sequence: int,
            arrival_time: datetime,
            departure_time: datetime,
            timepoint: int
    ):
        self.stop_id: int = stop_id
        self.stop_code: int = stop_code
        self.stop_name: str = stop_name
        self.stop_desc: str = stop_desc
        self.stop_lat: float = stop_lat
        self.stop_lon: float = stop_lon
        self.location_type: int = location_type
        self.stop_sequence: int = stop_sequence
        self.arrival_time: datetime = arrival_time
        self.departure_time: datetime = departure_time
        self.timepoint: int = timepoint

    def reset_departure_time_to_origin_date(self, *, day: int = 1) -> 'StopTimeWithStopDetail':
        self.departure_time = self.departure_time.replace(year=1970, month=1, day=day)

        return self

    def reset_arrival_time_to_origin_date(self, *, day: int = 1) -> 'StopTimeWithStopDetail':
        self.arrival_time = self.arrival_time.replace(year=1970, month=1, day=day)

        return self


"""

class RoutesByRouteShortNameWithTripsWithStopTimesResponse:
    route_id: int
    route_short_name: str
    route_long_name: str
    route_code: str
    trips: List['GetRouteByRouteShortNameWithTripsWithStopTimesResponse.Trip']

    class Trip:
        trip_id: int
        service_id: int
        trip_headsign: str
        direction_id: int
        stop_times: List['Trip.StopTimeWithStopDetails']

        class StopTimeWithStopDetails:
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


GetRoutesByRouteShortNameWithTripsWithStopTimesResponse = List[RoutesByRouteShortNameWithTripsWithStopTimesResponse]

{
    "RouteId": 2147483647,
    "AgencyId": 2147483647,
    "RouteShortName": "string",
    "RouteLongName": "string",
    "RouteType": 2147483647,
    "RouteDesc": "string",
    "RouteCode": "string",
    "Trips": [
      {
        "trip_id": 2147483647,
        "service_id": 2147483647,
        "trip_headsign": "string",
        "direction_id": 2147483647,
        "stops": [
          {
            "stop_id": 2147483647,
            "stop_code": "string",
            "stop_name": "string",
            "stop_desc": "string",
            "stop_lat": 0,
            "stop_lon": 0,
            "location_type": 2147483647,
            "stop_times": [
              {
                "id": 2147483647,
                "stop_sequence": 2147483647,
                "arrival_time": "2023-12-31T17:39:21.719Z",
                "departure_time": "2023-12-31T17:39:21.719Z",
                "timepoint": 2147483647
              }
            ]
          }
        ],
        "stop_times": [
          {
            "id": 2147483647,
            "stop": {
              "stop_id": 2147483647,
              "stop_code": "string",
              "stop_name": "string",
              "stop_desc": "string",
              "stop_lat": 0,
              "stop_lon": 0,
              "location_type": 2147483647
            },
            "stop_sequence": 2147483647,
            "arrival_time": "2023-12-31T17:39:21.719Z",
            "departure_time": "2023-12-31T17:39:21.719Z",
            "timepoint": 2147483647
          }
        ]
      }
    ]
  }

bus_coordinates_by_time = {
    "type": "FeatureCollection",
    "features": []
}

feature = {
    'type': 'Feature',
    'properties': {
        'vendor': 'iett'
    },
    'geometry': {
        'type': 'LineString',
        'coordinates': coordinates
    },
    'id': '76y'
}


"""
