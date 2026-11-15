import json
import math
import os.path
from typing import Dict
from typing import List
from typing import Optional

import orjson
from loguru import logger
from tortoise import run_async

from src.clients import TortoiseOrm
from src.config.csvfiles import GTFS_RESOURCE_DIRECTORY_PATH
from src.repositories import route_path_repository

ROUTE_PATHS_GEOJSON_PATH: str = os.path.join(GTFS_RESOURCE_DIRECTORY_PATH, 'iett-hat-guzergahlari.geojson')
DIRECTION_IDS_BY_YON: Dict[str, int] = {'GİDİŞ': 0, 'DÖNÜŞ': 1}
SIMPLIFY_TOLERANCE_IN_METERS: float = 5.0
COORDINATE_DECIMALS: int = 5
METERS_PER_DEGREE: float = math.radians(1) * 6371000.0


def map_feature_to_route_path(feature: Dict) -> Optional[Dict]:
    properties: Dict = feature['properties']
    geometry: Dict = feature.get('geometry') or {}
    if geometry.get('type') != 'LineString' or len(geometry['coordinates']) < 2:
        return None

    coordinates = simplify_line(geometry['coordinates'], SIMPLIFY_TOLERANCE_IN_METERS)

    return {
        'route_path_id': int(properties['ID']),
        'route_code': properties['GUZERGAH_KODU'],
        'route_short_name': properties['HAT_KODU'],
        'direction_id': DIRECTION_IDS_BY_YON.get(properties['YON']),
        'departure_no': int(properties['DEPAR_NO']),
        'length_in_meters': float(properties['UZUNLUK'].replace(',', '.')),
        'coordinates': orjson.dumps([
            [round(longitude, COORDINATE_DECIMALS), round(latitude, COORDINATE_DECIMALS)]
            for longitude, latitude in coordinates
        ]).decode()
    }


def simplify_line(coordinates: List[List[float]], tolerance_in_meters: float) -> List[List[float]]:
    longitude_scale = math.cos(math.radians(coordinates[0][1]))
    points = [(coordinate[0] * longitude_scale * METERS_PER_DEGREE, coordinate[1] * METERS_PER_DEGREE) for coordinate in coordinates]
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    ranges = [(0, len(points) - 1)]
    while ranges:
        first, last = ranges.pop()
        farthest_index, farthest_distance = first, 0.0
        for index in range(first + 1, last):
            distance = _distance_to_segment(points[index], points[first], points[last])
            if distance > farthest_distance:
                farthest_index, farthest_distance = index, distance
        if farthest_distance > tolerance_in_meters:
            keep[farthest_index] = True
            ranges.append((first, farthest_index))
            ranges.append((farthest_index, last))

    return [coordinate[:2] for coordinate, is_kept in zip(coordinates, keep) if is_kept]


async def save_route_paths(batch_size: int = 500):
    with open(ROUTE_PATHS_GEOJSON_PATH, encoding='utf-8') as geojson_file:
        features: List[Dict] = json.load(geojson_file)['features']
    logger.info(f'Read {len(features)} route path features from GeoJSON...')

    route_paths: List[Dict] = [route_path for route_path in map(map_feature_to_route_path, features) if route_path]
    logger.info(f'Mapped {len(route_paths)} route paths, saving to SQLite...')
    await route_path_repository.delete_all()
    for start in range(0, len(route_paths), batch_size):
        await route_path_repository.create_many(route_paths[start:start + batch_size])
    logger.info('Route paths saved to SQLite successfully!')


async def run():
    await TortoiseOrm.init()
    await save_route_paths()
    await TortoiseOrm.close()


def _distance_to_segment(point, start, end) -> float:
    dx, dy = end[0] - start[0], end[1] - start[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return math.hypot(point[0] - start[0], point[1] - start[1])
    fraction = max(0.0, min(1.0, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_squared))

    return math.hypot(point[0] - (start[0] + fraction * dx), point[1] - (start[1] + fraction * dy))


if __name__ == "__main__":
    run_async(run())
