import pygame

from Tile import Tile
import math
from perlin_noise import PerlinNoise
import random
from Data.TilesData import TilesData


class Field:
    def __init__(self, screen, hex_width=25, field_size=None, hex_amount=None):
        if hex_width == 'auto':  # if auto was entered calculate the hex width
            if field_size is None or hex_amount is None:
                print(f"Field could not be initialized, because field_size or hex_amount is none!!!")
                return

            # calculate the sizes of the hexagons with the field size
            self.hex_width = (field_size[0] / hex_amount[0]) * 4 / 3
            self.hex_size = self.hex_width / 2
            hex_height = round(math.sqrt(3) * self.hex_size)
            self.hex_size = round(self.hex_size)
            self.hex_width = round(self.hex_width)

            # calculate how many hexagons exactly fit in the field
            if hex_amount[1] == 0:
                hex_amount = (hex_amount[0], int(hex_amount[0] * (field_size[1] / field_size[0])) - 3)

            # st the current hex size
            self.field_size = hex_amount
        else:
            # if the hex width was given, calculate the size, height.
            self.hex_width = hex_width
            self.hex_size = hex_width / 2
            hex_height = round(math.sqrt(3) * self.hex_size)
            self.hex_size = round(self.hex_size)

            # calculate how many hexagons of the given size fit in the field
            self.field_size = (
                math.ceil((field_size[0] + self.hex_width / 4) / (self.hex_width + self.hex_width / 2) * 2),
                math.ceil(field_size[1] / hex_height) + 1)

        self.tiles = []
        self.screen = screen
        y_offset = 0

        # initialize the sprite dictionary, it can't be a constant because the .convert_alpha can't be called before the screen is loaded
        tiles_data = TilesData()

        # scale all the sprites to fit the hexagonal sprites
        for key, sprite in tiles_data.sprite_dict.items():
            if isinstance(sprite, list):  # if a given item has multiple sprites, scale all of them
                for i, element in enumerate(sprite):
                    width = self.hex_width
                    height = round(self.hex_width * element.get_height() / element.get_width())  # keep ratio
                    tiles_data.sprite_dict[key][i] = pygame.transform.scale(element, (width, height))
            else:  # otherwise just scale the single sprite
                width = self.hex_width
                height = round(self.hex_width * sprite.get_height() / sprite.get_width())  # keep ratio
                tiles_data.sprite_dict[key] = pygame.transform.scale(sprite, (width, height))

        # generate the noise for the terrain and resources
        noise = PerlinNoise(octaves=1, seed=random.randint(1, 200))
        resource_noise = PerlinNoise(octaves=2, seed=random.randint(1, 200))

        # calculate the points of a hexagon with the unit circle
        points = [[self.hex_size * math.cos((2 * math.pi) / 6 * i), self.hex_size * math.sin((2 * math.pi) / 6 * i)] for i in range(1, 7)]

        # fill the field with hexagons
        for x in range(0, self.field_size[0]):
            self.tiles.append([])
            for y in range(0, self.field_size[1]):
                self.tiles[x].append(
                    Tile(pos=(x * round(self.hex_width * (3 / 4)) + self.hex_width / 4, y * hex_height - hex_height / 2 + y_offset), place=(x, y),
                         size=(self.hex_width, hex_height), radius=self.hex_size, points=points, screen=screen, noise=noise,
                         resource_noise=resource_noise, sprite_dict=tiles_data.sprite_dict, field=self))

            y_offset = hex_height / 2 if x % 2 == 0 else 0

        # initialize all the tiles, this allows them to find their neighbours for the AI
        for tiles in self.tiles:
            for tile in tiles:
                tile.init(self.tiles, self.field_size)

        # make a separate list for the water and land tiles so they can be rendered separately, greatly improving frame rate
        self.tiles_list = []
        self.water_tiles = []
        for tiles in self.tiles:
            for tile in tiles:
                if not tile.is_water:
                    self.tiles_list.append(tile)
                else:
                    self.water_tiles.append(tile)

        # sort the tiles from top left to bottom right so they don't render over each other
        self.tiles_list.sort()
        self.water_tiles.sort()

        # create sprite groups and add the sprites to them
        self.tiles_group = pygame.sprite.Group()
        self.tiles_group.add(self.tiles_list)
        self.water_group = pygame.sprite.Group()
        self.water_group.add(self.water_tiles)

        # draw the water sprites on the screen
        self.water_group.draw(screen.get_screen())

        print(f"Field has been generated, {self.hex_size = }, {len(self.tiles) = }, {self.field_size = }")

    # TODO fix deze naam
    def display(self, screen):  # render and update the land tiles
        self.tiles_group.update()
        self.tiles_group.draw(screen.get_screen())

        # for tile_row in self.tiles:
        #     for tile in tile_row:
        #         pass

    def update_water(self):  # update the water tiles
        self.water_group.draw(self.screen.get_screen())

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

    def get_tile_from_point(self, point):
        for tile_row in self.tiles:
            for tile in tile_row:
                if tile.isOver(point):
                    return tile
