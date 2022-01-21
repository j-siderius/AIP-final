from enum import Enum

# a place to store settings and constants, might make a separate JSON file to actual store settings
# TODO
#   - dict maken met alles tiles en walk speed enzo
#   - dict maken met structes enz.

class Settings:
    WATER_DROP_OFF_SCALING = 1
    PLAYER_WALKING_TIME = 0.25
    WOODEN_WALL_COST = 2

    HIGHLIGHT_COLOR = (255, 100)
    HIGHLIGHT_COLOR_SELECTED = (255, 140, 0, 200)
    HIGHLIGHT_COLOR_ACTION = (65, 105, 225, 150)


class ResourceTiles(Enum):
    none = -1
    forest = 0
    large_forest = 1
    rock = 2
    large_rock = 3


class Resources(Enum):
    wood = "Wood"
    stone = "Stone"


# for the future, not used yet
class Structures(Enum):
    wooden_wall = "Wooden wall"
    stone_wall = "Stone wall"


class MouseButton:
    left: int = 1
    scroll: int = 2
    right: int = 3
    scroll_up: int = 4
    scroll_down: int = 5
