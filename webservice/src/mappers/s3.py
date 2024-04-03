from typing import Dict

from src.models.deck import DeckGLRoutesWithTripGeometries
from src.models.dto.s3 import DeckGLRouteTripGeometriesByRouteShortNameObject


def map_routes_with_trip_geometries_to_deck_gl_route_trip_geometries_by_route_short_name_object(
        deck_gl_routes_with_trip_geometries: DeckGLRoutesWithTripGeometries
) -> DeckGLRouteTripGeometriesByRouteShortNameObject:
    trip_details_by_trip_ids: Dict[int, DeckGLRouteTripGeometriesByRouteShortNameObject.TripDetails] = {}
    for trip_id, trip_geometry in deck_gl_routes_with_trip_geometries.trip_geometries_by_trip_ids.items():
        trip_details_by_trip_ids[trip_id] = DeckGLRouteTripGeometriesByRouteShortNameObject.TripDetails(
            trip_id=trip_id,
            route_id=trip_geometry.properties['route_id'],
            departure_time=trip_geometry.coordinates[0][3]
        )

    return DeckGLRouteTripGeometriesByRouteShortNameObject(
        route_short_name=deck_gl_routes_with_trip_geometries.route_short_name,
        trip_ids_by_path_ids=deck_gl_routes_with_trip_geometries.trip_ids_by_path_ids,
        path_coordinates_by_path_ids=deck_gl_routes_with_trip_geometries.path_coordinates_by_path_ids,
        path_timestamp_difference_by_path_ids=deck_gl_routes_with_trip_geometries.path_timestamp_difference_by_path_ids,
        trip_details_by_trip_ids=trip_details_by_trip_ids
    )
