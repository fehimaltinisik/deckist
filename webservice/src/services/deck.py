from typing import List

from src.exceptions.s3 import S3UploadException
from src.entities.gtfs import Route
from src.models.route import RoutesWithTripGeometries
from src.services import route as route_service
from src.services import s3 as s3service


async def get_trip_layer_geometries_by_route_short_name(route_short_name: str) -> RoutesWithTripGeometries:
    routes_with_trip_geometries: RoutesWithTripGeometries = await route_service.get_routes_with_trip_geometries_by_route_short_name(
        route_short_name)

    return routes_with_trip_geometries


async def upload_route_coordinates_by_route_short_name_to_s3(route_short_name: str):
    routes_with_trip_geometries: RoutesWithTripGeometries = await route_service.get_routes_with_trip_geometries_by_route_short_name(
        route_short_name)
    status: bool = s3service.upload_routes_with_trip_geometries_to_s3_as_route_segments_file_object(
        route_short_name=route_short_name, routes_with_trip_geometries=routes_with_trip_geometries)

    if not status:
        raise S3UploadException(f"Failed to upload {route_short_name} geometries to S3")


async def get_routes_by_route_short_name(route_short_name: str) -> List[Route]:
    routes: List[Route] = await route_service.get_routes_by_route_short_name(
        route_short_name)

    return routes
