from typing import Dict
from typing import List

from loguru import logger
from tortoise.expressions import Subquery
from tortoise.query_utils import Prefetch

from src.entities.gtfs import Route
from src.entities.gtfs import Shape
from src.entities.gtfs import StopTime
from src.entities.gtfs import Trip


async def create_many(items: List[Dict]) -> List[Route]:
    objects: List[Route] = [Route(**item) for item in items]
    records: List[Route] = await Route.bulk_create(objects, batch_size=1000)
    logger.info(f"Created {len(records)} Route records!")

    return records


async def find_by_id(route_id: int) -> Route:
    route: Route = await Route.get(route_id=route_id)

    return route


async def find_by_short_name(route_short_name: str) -> List[Route]:
    routes: List[Route] = await Route.filter(route_short_name=route_short_name)

    return routes


async def find_by_short_name_with_trips_with_stop_times(route_short_name: str) -> List[Route]:
    queryset = Route.filter(route_short_name=route_short_name).all().prefetch_related(
        Prefetch('trips', queryset=Trip.all()),
        Prefetch('trips__stop_times', queryset=StopTime.all().select_related('stop'))
    )

    routes: List[Route] = await queryset

    return routes
