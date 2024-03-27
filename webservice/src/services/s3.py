import logging
import os
from io import BytesIO

import boto3
import orjson
from botocore.exceptions import ClientError

from src.mappers.s3 import map_routes_with_trip_geometries_to_deck_route_segments
from src.models.dto.s3 import DeckRouteSegments
from src.models.route import RoutesWithTripGeometries

S3_CLIENT = boto3.client('s3')
S3_BUCKET = os.environ.get('S3_BUCKET', 'deckist')


def upload_routes_with_trip_geometries_to_s3_as_route_segments_file_object(
        route_short_name: str,
        routes_with_trip_geometries: RoutesWithTripGeometries) -> bool:
    deck_route_segments: DeckRouteSegments = map_routes_with_trip_geometries_to_deck_route_segments(
        routes_with_trip_geometries)

    try:
        with BytesIO(orjson.dumps(deck_route_segments.dict(by_alias=True).get('__root__', []))) as stream:
            S3_CLIENT.upload_fileobj(stream, S3_BUCKET, f"deck/{route_short_name}-route.json")

    except ClientError as e:
        logging.exception(e)

        return False

    return True
