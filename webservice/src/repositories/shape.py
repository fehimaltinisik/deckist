from typing import Dict
from typing import List

from loguru import logger

from src.entities.gtfs import Shape


async def create_many(items: List[Dict]) -> List[Shape]:
    objects: List[Shape] = [Shape(**item) for item in items]
    records: List[Shape] = await Shape.bulk_create(objects, batch_size=1000)

    logger.info(f"Created {len(records)} Shape records!")

    return records


async def find_by_ids(shape_ids: List[int]) -> List[Shape]:
    shapes: List[Shape] = await Shape.filter(shape_id__in=shape_ids)

    return shapes
