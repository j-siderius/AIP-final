import pygame

from Tile import Tile
import math
from perlin_noise import PerlinNoise
import random


class Field:
    def __init__(self, screen, hex_width=25, field_pos=(0, 0), field_size=None, hex_amount=None):
        print(f"{field_size = }")
        if hex_width == 'auto':
            if field_size is None or hex_amount is None:
                print(f"Field could not be initialized, because field_size or hex_amount is none!!!")
                return

            hex_width = (field_size[0] / hex_amount[0]) * 4/3
            hex_size = hex_width / 2
            hex_height = round(math.sqrt(3) * hex_size)
            hex_size = round(hex_size)
            hex_width = round(hex_width)

            if hex_amount[1] == 0:
                hex_amount = (hex_amount[0], int(hex_amount[0] * (field_size[1] / field_size[0]))-3)

            field_size = hex_amount
        else:
            hex_size = hex_width / 2
            hex_height = round(math.sqrt(3) * hex_size)
            hex_size = round(hex_size)
            field_size = (math.ceil((field_size[0] + hex_width/4) / (hex_width + hex_width/2) * 2), math.ceil(field_size[1] / hex_height)+1)

        self.tiles = []
        self.screen = screen
        y_offset = 0

        sprite_dict = {
            "deep_water": pygame.image.load("./Sprites/Borderless_Tilles/deep_water.png").convert_alpha(),
            "water": pygame.image.load("./Sprites/Borderless_Tilles/water.png").convert_alpha(),
            "grass": pygame.image.load("./Sprites/Tiles/grass.png").convert_alpha(),
            "hills": pygame.image.load("./Sprites/Tiles/hills.png").convert_alpha(),
            "mountain": pygame.image.load("./Sprites/Tiles/mountain.png").convert_alpha(),
            "SmallerMountain": pygame.image.load("./Sprites/Tiles/SmallerMountain.png").convert_alpha(),
            # "snow": pygame.image.load("./Sprites/Tiles/snow.png"),

            "selected_grass": pygame.image.load("./Sprites/Selected_tilles/grass.png").convert_alpha(),
            "selected_hills": pygame.image.load("./Sprites/Selected_tilles/hills.png").convert_alpha(),
        }
        for key, sprite in sprite_dict.items():
            width = hex_width
            height = round(hex_width * sprite.get_height() / sprite.get_width())  # keep ratio
            sprite_dict[key] = pygame.transform.scale(sprite, (width, height))

        noise = PerlinNoise(octaves=1, seed=random.randint(1, 100))

        points = [[hex_size * math.cos((2 * math.pi) / 6 * i), hex_size * math.sin((2 * math.pi) / 6 * i)] for i in range(1, 7)]

        for x in range(0, field_size[0]):
            self.tiles.append([])
            for y in range(0, field_size[1]):
                # self.tiles[x].append(
                #     Tile((x * hex_width*(3/4) + hex_size / 2 + field_pos[0], y * hex_height + y_offset + hex_height / 2 + field_pos[1]), (x, y)
                #          , hex_size, points, screen, noise, sprite_dict))

                self.tiles[x].append(
                    Tile(pos=(x * round(hex_width * (3/4)) + hex_width/4, y * hex_height - hex_height/2 + y_offset), place=(x, y),
                         size=(hex_width, hex_height), radius=hex_size, points=points, screen=screen, noise=noise, sprite_dict=sprite_dict))

            y_offset = hex_height / 2 if x % 2 == 0 else 0

        for tiles in self.tiles:
            for tile in tiles:
                tile.init(self.tiles, field_size)

        self.tiles_list = []
        self.water_tiles = []
        for tiles in self.tiles:
            for tile in tiles:
                if not tile.isWater:
                    self.tiles_list.append(tile)
                else:
                    self.water_tiles.append(tile)

        self.tiles_list.sort()
        self.water_tiles.sort()

        self.tiles_group = pygame.sprite.Group()
        self.tiles_group.add(self.tiles_list)
        self.water_group = pygame.sprite.Group()
        self.water_group.add(self.water_tiles)

        self.water_group.draw(screen.get_screen())

        print(f"{hex_size = }, {len(self.tiles) = }, {field_size = }")

        self.hex_size = hex_size
        self.hex_width = hex_width

    def display(self, screen):
        self.tiles_group.draw(screen.get_screen())
        self.tiles_group.update(screen.get_mouse_pos())
        # for tile_row in self.tiles:
        #     for tile in tile_row:
        #         tile.display()
        #
        # for tile_row in self.tiles:
        #     for tile in tile_row:
        #         tile.mouse_pointer(self.screen.get_mouse_pos())

    # returns the tile object at given coordinates
    def get_tile(self, tileX, tileY):
        return self.tiles[int(tileX)][int(tileY)]

    # returns the size of a hex (to base other objects off of)
    def get_hex_size(self):
        return self.hex_size

    def get_hex_width(self):
        return self.hex_width

    def highlight_tile(self, tileX, tileY):
        self.tiles[tileX][tileY].highlight()

    def get_current_mouse_tile(self):
        for tile_row in self.tiles:
            for tile in tile_row:
                if tile.isOver(self.screen.get_mouse_pos()):
                    return tile
