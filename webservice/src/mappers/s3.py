from src.models.dto.s3 import DeckRouteSegments
from src.models.route import RoutesWithTripGeometries


def map_routes_with_trip_geometries_to_deck_route_segments(
        route_with_trip_geometries: RoutesWithTripGeometries) -> DeckRouteSegments:
    route_segments = []
    for trip_geometry in route_with_trip_geometries.trip_geometries:
        coordinates = [[coordinate[0], coordinate[1]] for coordinate in trip_geometry.coordinates]
        timestamps = [coordinate[3] for coordinate in trip_geometry.coordinates]
        route_segments.append(
            {
                'trip_id': trip_geometry.properties['trip_id'],
                'route_id': trip_geometry.properties['route_id'],
                'route_short_name': trip_geometry.properties['route_short_name'],
                'path': coordinates,
                'timestamps': timestamps
            }
        )

    return DeckRouteSegments.parse_obj(route_segments)
