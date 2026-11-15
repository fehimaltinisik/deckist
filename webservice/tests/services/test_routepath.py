from typing import Optional

from src.entities.gtfs import Route
from src.entities.gtfs import RoutePath
from src.services import routepath as route_path_service


def _route_path(route_path_id: int, route_code: str, direction_id: int, departure_no: int, length_in_meters: float) -> RoutePath:
    return RoutePath(
        route_path_id=route_path_id,
        route_code=route_code,
        route_short_name='500T',
        direction_id=direction_id,
        departure_no=departure_no,
        length_in_meters=length_in_meters,
        coordinates='[]'
    )


def _route(route_code: Optional[str]) -> Route:
    return Route(route_id=1, agency_id=1, route_short_name='500T', route_long_name='', route_type=3, route_desc='', route_code=route_code)


ROUTE_PATHS = [
    _route_path(1, '500T_G_D1588', 0, 1588, 72963.0),
    _route_path(2, '500T_G_D0', 0, 0, 56930.0),
    _route_path(3, '500T_D_D0', 1, 0, 56058.0),
    _route_path(4, '500T_D_D6377', 1, 6377, 76168.0),
]


class TestSelectRoutePath:
    def test_given_matching_route_code_when_selected_then_returns_exact_route_path(self):
        route = _route('500T_G_D1588')

        route_path = route_path_service.select_route_path(route, 0, ROUTE_PATHS)

        assert route_path.route_path_id == 1

    def test_given_unknown_route_code_when_selected_then_prefers_main_departure_in_same_direction(self):
        route = _route('500T_D_D9999')

        route_path = route_path_service.select_route_path(route, 1, ROUTE_PATHS)

        assert route_path.route_path_id == 3

    def test_given_no_main_departure_when_selected_then_prefers_longest_route_path(self):
        route_paths = [path for path in ROUTE_PATHS if path.departure_no != 0] + [_route_path(5, '500T_D_D7000', 1, 7000, 80000.0)]

        route_path = route_path_service.select_route_path(_route(None), 1, route_paths)

        assert route_path.route_path_id == 5

    def test_given_equal_candidates_when_selected_then_lowest_route_code_wins(self):
        route_paths = [_route_path(6, '500T_G_D2', 0, 2, 100.0), _route_path(7, '500T_G_D1', 0, 1, 100.0)]

        route_path = route_path_service.select_route_path(_route(None), 0, route_paths)

        assert route_path.route_path_id == 7

    def test_given_no_route_path_in_direction_when_selected_then_returns_none(self):
        route_paths = [path for path in ROUTE_PATHS if path.direction_id == 0]

        route_path = route_path_service.select_route_path(_route(None), 1, route_paths)

        assert route_path is None
