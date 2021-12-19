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
            hex_width = (field_size[0]) / (hex_amount[0] - 0.34)
            hex_size = hex_width / (1.5 * math.cos(0)) * 2

            if hex_amount[1] == 0:
                hex_amount = (hex_amount[0], int(hex_amount[0] * (field_size[1] / field_size[0])) - 3)
            field_size = hex_amount
            field_pos = (field_pos[0] - hex_size / 4, field_pos[1] - hex_size / 2)
        else:
            field_size = (23, 20)

        self.tiles = []
        self.screen = screen
        y_offset = 0
        hex_size = hex_width / (1.5 * math.cos(0)) * 2
        hex_height = hex_size * math.sin((2 * math.pi) / 3)

        noise = PerlinNoise(octaves=1, seed=random.randint(1, 100))

        points = [[hex_size / 2 * math.cos((2 * math.pi) / 6 * i), hex_size / 2 * math.sin((2 * math.pi) / 6 * i)] for i in range(1, 7)]

        for x in range(0, field_size[0]):
            self.tiles.append([])
            for y in range(0, field_size[1]):
                self.tiles[x].append(
                    Tile((x * hex_width + hex_size / 2 + field_pos[0], y * hex_height + y_offset + hex_height / 2 + field_pos[1]), (x, y)
                         , hex_size, points, screen, noise))

            y_offset = hex_height / 2 if x % 2 == 0 else 0

        for tiles in self.tiles:
            for tile in tiles:
                tile.init(self.tiles, field_size)

        self.hex_size = hex_size
        self.hex_width = hex_width

        print(f"{self.hex_size = }, {len(self.tiles) = }, {field_size = }")

    def display(self):
        for tile_row in self.tiles:
            for tile in tile_row:
                tile.display()

        for tile_row in self.tiles:
            for tile in tile_row:
                tile.debug(self.screen.get_mouse_pos())

    # returns the tile object at given coordinates
    def get_tile(self, tileX, tileY):
        return self.tiles[tileX][tileY]

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
                if tile.debug(self.screen.get_mouse_pos()):
                    return tile
