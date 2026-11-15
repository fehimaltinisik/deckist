import pytest

from src.models.polyline import RoutePathProjection

COORDINATES = [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0], [3.0, 0.0]]
CUMULATIVE_DISTANCES = [0.0, 10.0, 20.0, 30.0]


class TestRoutePathProjectionTrim:
    def test_given_projection_when_trimmed_then_vertices_start_and_end_at_stops(self):
        projection = RoutePathProjection(coordinates=COORDINATES, cumulative_distances=CUMULATIVE_DISTANCES, stop_distances=[5.0, 25.0])

        vertices = projection.trim()

        assert [coordinate for coordinate, _ in vertices] == [[0.5, 0.0], [1.0, 0.0], [2.0, 0.0], [2.5, 0.0]]
        assert [distance for _, distance in vertices] == [5.0, 10.0, 20.0, 25.0]


class TestRoutePathProjectionProgressVertices:
    def test_given_projection_when_progress_read_then_it_runs_from_zero_to_one(self):
        projection = RoutePathProjection(coordinates=COORDINATES, cumulative_distances=CUMULATIVE_DISTANCES, stop_distances=[5.0, 25.0])

        progress = [progress for _, progress in projection.progress_vertices]

        assert progress == pytest.approx([0.0, 0.25, 0.75, 1.0])
