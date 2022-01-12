import pygame


class TilesData:

    sprite_dict = {
        "grass": pygame.image.load("Data/Sprites/Tiles/grass.png").convert_alpha(),
        "hills": [pygame.image.load("Data/Sprites/Tiles/hills.png").convert_alpha(),
                  pygame.image.load("Data/Sprites/Tiles/hills2.png").convert_alpha()],
        "mountain": pygame.image.load("Data/Sprites/Tiles/mountain.png").convert_alpha(),

        # water
        "water": [pygame.image.load(f"Data/Sprites/water/water{i}.png").convert_alpha() for i in range(0, 8)],

        # resources:
        "forest_grass": pygame.image.load("Data/Sprites/Tiles/forest.png").convert_alpha(),
        "large_forest_grass": pygame.image.load("Data/Sprites/Tiles/large_forest.png").convert_alpha(),
        "forest_hills": [pygame.image.load("Data/Sprites/Tiles/foresthills.png").convert_alpha(),
                         pygame.image.load("Data/Sprites/Tiles/foresthills2.png").convert_alpha()],

        # highlighted tiles:
        "selected_grass": pygame.image.load("Data/Sprites/Selected_tilles/grass.png").convert_alpha(),
        "selected_hills": [pygame.image.load("Data/Sprites/Selected_tilles/hills.png").convert_alpha(),
                           pygame.image.load("Data/Sprites/Selected_tilles/hills2.png").convert_alpha()],
        "selected_forest_grass": pygame.image.load("Data/Sprites/Selected_tilles/forest.png").convert_alpha(),
        "selected_large_forest_grass": pygame.image.load("Data/Sprites/Selected_tilles/large_forest.png").convert_alpha(),
        "selected_forest_hills": [pygame.image.load("Data/Sprites/Selected_tilles/foresthills.png").convert_alpha(),
                                  pygame.image.load("Data/Sprites/Selected_tilles/foresthills2.png").convert_alpha()],

        # new highlights
        # "is_highlight": pygame.image.load("./Sprites/Selected_tilles/highlight-white.png").convert_alpha(),

        # structures
        "wall_grass": pygame.image.load("Data/Sprites/Tiles/wall_grass.png").convert_alpha(),
        "wall_hills": pygame.image.load("Data/Sprites/Tiles/wall_hills2.png").convert_alpha()
    }

    Tiles = {
        "grass": {
            "sprite": pygame.image.load("Data/Sprites/Tiles/grass.png").convert_alpha(),
            "walkspeed": 1,
            "walkable": True
        },
        "hills": [pygame.image.load("Data/Sprites/Tiles/hills.png").convert_alpha(),
                  pygame.image.load("Data/Sprites/Tiles/hills2.png").convert_alpha()],
        "mountain": pygame.image.load("Data/Sprites/Tiles/mountain.png").convert_alpha(),

        # water
        "water": [pygame.image.load(f"Data/Sprites/water/water{i}.png").convert_alpha() for i in range(0, 8)],

        # resources:
        "forest_grass": pygame.image.load("Data/Sprites/Tiles/forest.png").convert_alpha(),
        "large_forest_grass": pygame.image.load("Data/Sprites/Tiles/large_forest.png").convert_alpha(),
        "forest_hills": [pygame.image.load("Data/Sprites/Tiles/foresthills.png").convert_alpha(),
                         pygame.image.load("Data/Sprites/Tiles/foresthills2.png").convert_alpha()],
        # structures
        "wall_grass": pygame.image.load("Data/Sprites/Tiles/wall_grass.png").convert_alpha(),
        "wall_hills": pygame.image.load("Data/Sprites/Tiles/wall_hills2.png").convert_alpha()
    }
