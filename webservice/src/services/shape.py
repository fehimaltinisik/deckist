from typing import List

from src.entities.gtfs import Shape
from src.repositories import shape_repository


async def get_shapes_by_ids(shape_ids: List[int]) -> List[Shape]:
    shapes: List[Shape] = await shape_repository.find_by_ids(shape_ids)

    return shapes
