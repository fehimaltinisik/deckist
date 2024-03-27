from typing import Dict
from typing import List

from loguru import logger

from src.entities.gtfs import Trip


async def create_many(items: List[Dict]) -> List[Trip]:
    objects: List[Trip] = [Trip(**item) for item in items]
    records: List[Trip] = await Trip.bulk_create(objects, batch_size=1000)

    logger.info(f"Created {len(records)} Trip records!")

    return records
