import pygame
from Data.settings import *


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
    def __init__(self, walkspeed=0, walkable=True, hitpoints=0, resource=ResourceTiles.none):
        self.walkspeed = walkspeed
        self.walkable = walkable
        self.hitpoints = hitpoints
        self.resource = resource

    def copy(self):
        return TileProperty(self.walkspeed, self.walkable, self.hitpoints, self.resource)

# dictionary that houses all the information about the tiles
tiles_dict = {
    # ground tiles:
    "grass": TileProperty(walkspeed=1),
    "hills": TileProperty(walkspeed=1),
    "mountain": TileProperty(walkable=False),

    # water tiles:
    "water": TileProperty(walkable=False),

    # resources:
    "forest_grass": TileProperty(walkspeed=1, resource=ResourceTiles.forest),
    "forest_hills": TileProperty(walkspeed=1, resource=ResourceTiles.forest),
    "large_forest_grass": TileProperty(walkspeed=1, resource=ResourceTiles.large_forest),

    # structures
    "wall_grass": TileProperty(walkable=False, hitpoints=100),
    "wall_hills": TileProperty(walkable=False, hitpoints=100),
}

# tiles_dict = {
#     # ground tiles:
#     "grass": {
#         "walkspeed": 1,
#         "walkable": True,
#         "resource": ResourceTiles.none,
#     },
#     "hills": {
#         "walkspeed": 1,
#         "walkable": True,
#         "resource": ResourceTiles.none,
#     },
#     "mountain": {
#         "walkspeed": 1,
#         "walkable": True,
#         "resource": ResourceTiles.none,
#     },
#
#     # water tiles:
#     "water": {
#         "walkspeed": 0,
#         "walkable": False,
#         "resource": ResourceTiles.none,
#     },
#
#     # resources:
#     "forest_grass": {
#         "walkspeed": 1,
#         "walkable": True,
#         "resource": ResourceTiles.forest,
#     },
#     "forest_hills": {
#         "walkspeed": 1,
#         "walkable": True,
#         "resource": ResourceTiles.forest,
#     },
#     "large_forest_grass": {
#         "walkspeed": 1,
#         "walkable": True,
#         "resource": ResourceTiles.large_forest,
#     },
#
#     # structures
#     "wall_grass": {
#         "walkspeed": 0,
#         "walkable": False,
#         "hitpoints": 100,
#     },
#     "wall_hills": {
#         "walkspeed": 0,
#         "walkable": False,
#         "hitpoints": 100,
#     },
# }

