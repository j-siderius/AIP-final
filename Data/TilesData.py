from enum import Enum

import pygame
# from Data.settings import *


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


class TilesData:
    def __init__(self):
        # dictionary housing al of the sprites for the tiles
        self.sprite_dict = {
            "grass": pygame.image.load("Data/Sprites/Tiles/grass.png").convert_alpha(),
            "hills": [pygame.image.load("Data/Sprites/Tiles/hills.png").convert_alpha(),
                      pygame.image.load("Data/Sprites/Tiles/hills2.png").convert_alpha()],
            "mountain": pygame.image.load("Data/Sprites/Tiles/mountain.png").convert_alpha(),

            # water
            "water": [pygame.image.load(f"Data/Sprites/water/water{i}.png").convert_alpha() for i in range(0, 8)],

            # resources:
            "forest_grass": pygame.image.load("Data/Sprites/Tiles/forest.png").convert_alpha(),
            "forest_hills": [pygame.image.load("Data/Sprites/Tiles/foresthills.png").convert_alpha(),
                             pygame.image.load("Data/Sprites/Tiles/foresthills2.png").convert_alpha()],
            "large_forest_grass": pygame.image.load("Data/Sprites/Tiles/large_forest.png").convert_alpha(),

            # structures
            "wall_grass": pygame.image.load("Data/Sprites/Tiles/wall_grass.png").convert_alpha(),
            "wall_hills": pygame.image.load("Data/Sprites/Tiles/wall_hills2.png").convert_alpha()
        }


class TileProperty:
    def __init__(self, walkspeed:float=0, walkable=True, hitpoints=0, resource_tile=ResourceTiles.none, resource=None, resource_amount=1, action_time: float = 0.25):
        self.walkspeed = walkspeed
        self.walkable = walkable
        self.hitpoints = hitpoints
        self.resource_tile = resource_tile
        self.resource = resource
        self.resource_amount = resource_amount
        self.action_time = action_time


# dictionary that houses all the information about the tiles
tiles_dict = {
    # ground tiles:
    "grass": TileProperty(walkspeed=1),
    "hills": TileProperty(walkspeed=1),
    "mountain": TileProperty(walkable=False),

    # water tiles:
    "water": TileProperty(walkable=False),

    # resources:
    "forest_grass": TileProperty(walkspeed=1, resource=Resources.wood, resource_tile=ResourceTiles.forest),
    "forest_hills": TileProperty(walkspeed=1, resource=Resources.wood, resource_tile=ResourceTiles.forest),
    "large_forest_grass": TileProperty(walkspeed=1, resource=Resources.wood, resource_tile=ResourceTiles.large_forest),

    # structures
    "wall_grass": TileProperty(walkable=False, hitpoints=3, resource=Resources.wood),
    "wall_hills": TileProperty(walkable=False, hitpoints=3, resource=Resources.wood),
}
