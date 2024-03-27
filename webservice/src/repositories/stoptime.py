from typing import Dict
from typing import List

from loguru import logger

from src.entities.gtfs import StopTime


async def create_many(items: List[Dict]) -> List[StopTime]:
    objects: List[StopTime] = [StopTime(**item) for item in items]
    records: List[StopTime] = await StopTime.bulk_create(objects, batch_size=1000)

    logger.info(f"Created {len(records)} StopTime records!")

    return records
