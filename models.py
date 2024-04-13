from dataclasses import dataclass
from enum import Enum


@dataclass
class RouteType(Enum):
    CAR = "car"
    # FOOT = "foot" # unavailable


@dataclass
class Route:
    id: int
    a_x: float
    a_y: float
    b_x: float
    b_y: float
