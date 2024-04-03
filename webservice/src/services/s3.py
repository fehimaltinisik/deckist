import logging
import os
from io import BytesIO
from typing import Optional

import boto3
import orjson
from botocore.exceptions import ClientError

from src.mappers.s3 import map_routes_with_trip_geometries_to_deck_gl_route_trip_geometries_by_route_short_name_object
from src.models.deck import DeckGLRoutesWithTripGeometries
from src.models.dto.s3 import DeckGLRouteTripGeometriesByRouteShortNameObject

S3_CLIENT = boto3.client('s3')
S3_BUCKET = os.environ.get('S3_BUCKET', 'deckist')


def upload_routes_with_trip_geometries_to_s3_as_route_segments_file_object(
        route_short_name: str,
        deck_gl_routes_with_trip_geometries: DeckGLRoutesWithTripGeometries
) -> None:
    deck_route_segments: DeckGLRouteTripGeometriesByRouteShortNameObject = map_routes_with_trip_geometries_to_deck_gl_route_trip_geometries_by_route_short_name_object(
        deck_gl_routes_with_trip_geometries
    )

    try:
        with BytesIO(orjson.dumps(deck_route_segments.dict(by_alias=True), option=orjson.OPT_NON_STR_KEYS)) as stream:
            S3_CLIENT.upload_fileobj(stream, S3_BUCKET, f"deck/{route_short_name}-route.json")

    except ClientError as e:
        logging.exception(e)


def download_routes_with_trip_geometries_from_s3_as_route_segments_file_object(route_short_name: str) -> Optional[DeckGLRouteTripGeometriesByRouteShortNameObject]:
    try:
        response = S3_CLIENT.get_object(Bucket=S3_BUCKET, Key=f"deck/{route_short_name}-route.json")
        deck_route_segments: DeckGLRouteTripGeometriesByRouteShortNameObject = DeckGLRouteTripGeometriesByRouteShortNameObject.parse_obj(
            orjson.loads(response['Body'].read())
        )

        return deck_route_segments

    except ClientError as e:
        logging.exception(e)

    return None
