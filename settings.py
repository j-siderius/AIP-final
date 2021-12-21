from enum import Enum

# a place to store settings and constants, might make a separate JSON file to actual store settings

class Settings:
    WATER_DROP_OFF_SCALING = 1


class ResourceTiles(Enum):
    none = -1
    forest = 0
    large_forest = 1
    rock = 2
    large_rock = 3


class Resources(Enum):
    wood = "Wood"
    stone = "Stone"
