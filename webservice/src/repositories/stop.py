from typing import Dict
from typing import List

from loguru import logger

from src.entities.gtfs import Stop


async def create_many(items: List[Dict]) -> List[Stop]:
    objects: List[Stop] = [Stop(**item) for item in items]
    records: List[Stop] = await Stop.bulk_create(objects, batch_size=1000)

    logger.info(f"Created {len(records)} Stop records!")

    return records
