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

            hex_width = (field_size[0] / hex_amount[0]) * 4/3  # (field_size[0]) / (hex_amount[0] - 0.34)
            # print(field_size, hex_amount, field_size[1] / hex_amount[1])
            hex_size = hex_width / 2  # hex_width / (1.5 * math.cos(0)) * 2
            hex_height = round(math.sqrt(3) * hex_size)
            hex_size = round(hex_size)
            hex_width = round(hex_width)


            # hex_height = field_size[1] / hex_amount[1]
            # hex_size = hex_height / math.sqrt(3)
            # hex_width = round(hex_size * 2)
            # hex_size = round(hex_size)
            # print(hex_height, hex_size, hex_width)

            if hex_amount[1] == 0:
                hex_amount = (hex_amount[0], int(hex_amount[0] * (field_size[1] / field_size[0]))-3)
            # if hex_amount[0] == 0:
            #     hex_amount = (int(hex_amount[1] * (field_size[0] / field_size[1])), hex_amount[1])

            field_size = hex_amount
            # field_pos = (field_pos[0] - hex_size / 4, field_pos[1] - hex_size / 2)
        else:
            hex_size = hex_width / 2  # / (1.5 * math.cos(0)) * 2
            hex_height = round(math.sqrt(3) * hex_size)
            hex_size = round(hex_size)
            field_size = (math.ceil(field_size[0] / (hex_width + hex_width/2) * 2), math.ceil(field_size[1] / hex_height)+1)

        self.tiles = []
        self.screen = screen
        y_offset = 0
        # hex_height = math.sqrt(3) * hex_size
        # hex_height = hex_size * math.sin((2 * math.pi) / 3)

        sprite_dict = {
            "deep_water": pygame.image.load("./Sprites/Borderless_Tilles/deep_water.png"),
            "water": pygame.image.load("./Sprites/Borderless_Tilles/water.png"),
            "grass": pygame.image.load("./Sprites/Tiles/grass.png"),
            "hills": pygame.image.load("./Sprites/Tiles/hills.png"),
            "mountain": pygame.image.load("./Sprites/Tiles/mountain.png"),
            "SmallerMountain": pygame.image.load("./Sprites/Tiles/SmallerMountain.png")
            # "snow": pygame.image.load("./Sprites/Tiles/snow.png"),
            # "deep_water": pygame.image.load("./Sprites/Other tiles/deep_water.png"),
            # "water": pygame.image.load("./Sprites/Other tiles/shallow_water.png"),
            # "grass": pygame.image.load("./Sprites/Other tiles/light_grass.png"),
            # "hills": pygame.image.load("./Sprites/Other tiles/dark_grass.png"),
            # "mountain": pygame.image.load("./Sprites/Other tiles/mountain.png"),
        }
        for key, sprite in sprite_dict.items():
            width = hex_width
            height = round(hex_width * sprite.get_height() / sprite.get_width())  # keep ratio
            # height = hex_height
            # width = hex_height * sprite.get_width() / sprite.get_height()
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
        for tiles in self.tiles:
            self.tiles_list.extend(tiles)
        self.tiles_list.sort()

        self.tiles_group = pygame.sprite.Group()
        self.tiles_group.add(self.tiles_list)

        print(f"{hex_size = }, {len(self.tiles) = }, {field_size = }")

    def display(self, screen):
        self.tiles_group.draw(screen.get_screen())
        self.tiles_group.update(screen.get_mouse_pos())
        # for tile_row in self.tiles:
        #     for tile in tile_row:
        #         tile.display()
        #
        # for tile_row in self.tiles:
        #     for tile in tile_row:
        #         tile.debug(self.screen.get_mouse_pos())
