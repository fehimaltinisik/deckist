from typing import List

from src.config.dto import DataTransferObject


class DeckRouteSegment(DataTransferObject):
    route_short_name: str
    trip_id: int
    route_id: int
    path: List[List[float]] = []
    timestamps: List[int] = []


class DeckRouteSegments(DataTransferObject):
    __root__: List[DeckRouteSegment]
