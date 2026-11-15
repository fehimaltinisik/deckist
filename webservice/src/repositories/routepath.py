from typing import Dict
from typing import List

from loguru import logger

from src.entities.gtfs import RoutePath


async def create_many(items: List[Dict]) -> List[RoutePath]:
    objects: List[RoutePath] = [RoutePath(**item) for item in items]
    records: List[RoutePath] = await RoutePath.bulk_create(objects, batch_size=1000)

    logger.info(f"Created {len(records)} RoutePath records!")

    return records


async def delete_all() -> None:
    deleted: int = await RoutePath.all().delete()

    logger.info(f"Deleted {deleted} RoutePath records!")


async def find_by_route_short_name(route_short_name: str) -> List[RoutePath]:
    route_paths: List[RoutePath] = await RoutePath.filter(route_short_name=route_short_name)

    return route_paths
