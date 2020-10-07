from math import sqrt
from typing import NamedTuple
from typing import Optional


class Location(NamedTuple):
    x: Optional[float]
    y: Optional[float]
    z: Optional[float] = 0.0


def get_distance_between_locations(location_1: Location, location_2: Location) -> float:
    return sqrt(
        ((location_1.x - location_2.x) ** 2)
        + ((location_1.y - location_2.y) ** 2)
        + ((location_1.z - location_2.z) ** 2)
    )
