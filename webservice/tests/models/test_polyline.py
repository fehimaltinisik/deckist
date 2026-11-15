import pytest

from src.models import polyline

STRAIGHT_PATH = [[29.00, 41.0], [29.01, 41.0], [29.02, 41.0], [29.03, 41.0]]
LOOP_PATH = [[29.00, 41.0], [29.01, 41.0], [29.01, 41.01], [29.00, 41.01], [29.00, 41.0002]]


class TestProjectStopsOntoRoutePath:
    def test_given_stops_near_path_when_projected_then_distances_increase_along_path(self):
        stops = [[29.0001, 41.0001], [29.015, 41.0002], [29.0299, 40.9999]]

        projection = polyline.project_stops_onto_route_path(stops, STRAIGHT_PATH)

        assert projection is not None
        assert projection.stop_distances == sorted(projection.stop_distances)
        assert projection.stop_distances[0] == pytest.approx(8.4, abs=1)
        assert projection.stop_distances[1] == pytest.approx(1260, abs=5)

    def test_given_stop_far_from_path_when_projected_then_returns_none(self):
        stops = [[29.0, 41.0], [29.015, 41.01], [29.03, 41.0]]

        projection = polyline.project_stops_onto_route_path(stops, STRAIGHT_PATH)

        assert projection is None

    def test_given_single_middle_outlier_among_many_stops_when_projected_then_outlier_is_skipped(self):
        stops = [[29.0 + 0.0025 * index, 41.0] for index in range(13)]
        stops[6] = [29.015, 41.01]

        projection = polyline.project_stops_onto_route_path(stops, STRAIGHT_PATH)

        assert projection is not None
        assert projection.stop_distances[6] == projection.stop_distances[5]
        assert projection.end_distance == pytest.approx(projection.cumulative_distances[-1], abs=1)

    def test_given_last_stop_far_from_path_when_projected_then_returns_none(self):
        stops = [[29.0 + 0.0025 * index, 41.0] for index in range(12)] + [[29.03, 41.01]]

        projection = polyline.project_stops_onto_route_path(stops, STRAIGHT_PATH)

        assert projection is None

    def test_given_loop_path_when_last_stop_is_near_start_then_it_projects_to_loop_end(self):
        stops = [[29.0, 41.0], [29.01, 41.005], [29.0, 41.0003]]

        projection = polyline.project_stops_onto_route_path(stops, LOOP_PATH)

        assert projection is not None
        assert projection.stop_distances[0] == pytest.approx(0, abs=1)
        assert projection.stop_distances[-1] > projection.stop_distances[1] > projection.stop_distances[0]

    def test_given_stops_in_reverse_order_when_projected_then_returns_none(self):
        stops = [[29.03, 41.0], [29.0, 41.0]]

        projection = polyline.project_stops_onto_route_path(stops, STRAIGHT_PATH)

        assert projection is None

    def test_given_express_stops_far_apart_when_projected_then_far_stop_is_still_found(self):
        long_path = [[29.0 + 0.001 * index, 41.0] for index in range(101)]
        stops = [[29.0, 41.0], [29.1, 41.0]]

        projection = polyline.project_stops_onto_route_path(stops, long_path)

        assert projection is not None
        assert projection.end_distance == pytest.approx(projection.cumulative_distances[-1], abs=1)


class TestRoutePathProjectionTrim:
    def test_given_projection_when_trimmed_then_vertices_start_and_end_at_stops(self):
        stops = [[29.005, 41.0], [29.025, 41.0]]
        projection = polyline.project_stops_onto_route_path(stops, STRAIGHT_PATH)

        vertices = projection.trim()

        coordinates = [coordinate for coordinate, _ in vertices]
        assert coordinates[0] == pytest.approx([29.005, 41.0])
        assert coordinates[-1] == pytest.approx([29.025, 41.0])
        assert coordinates[1:-1] == [[29.01, 41.0], [29.02, 41.0]]
        assert [distance for _, distance in vertices] == sorted(distance for _, distance in vertices)
