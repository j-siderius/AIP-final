import copy
import random

import numpy as np
from Screen import *
# import noise
from perlin_noise import PerlinNoise
import math


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, place, size, points, screen: Screen, noise: PerlinNoise, sprite_dict: dict):
        super().__init__()
        self.screen = screen
        self.size = size
        self.pos = np.array(pos)
        self.x = place[0]
        self.y = place[1]
        self.bordering_tiles = []
        self.walkable = False

        self.color = (0, 100, 0)
        # self.points = np.array(points) + pos
        self.stroke_color = (110, 110, 110)

        self.height = noise([self.pos[0] / 300 + 500, self.pos[1] / 300 + 450]) * 1.5

        # make the height drop off at the edges:
        width, height = self.screen.get_size()
        dist_center_x = abs(width / 2 - self.pos[0])
        dist_center_y = abs(height / 2 - self.pos[1])
        self.height -= (dist_center_x ** 2) / ((width * 0.5) ** 2) - 0.2
        self.height -= (dist_center_y ** 2) / ((height * 0.6) ** 2) - 0.2

        if (pos[1] < size or pos[1] > screen.get_height() - size) and self.height > 0:
            self.height -= 0.2
            if self.height > 0: self.height = 0

        # if self.height < -0.3:  # deep water
        #     self.image = sprite_dict["deep_water"].copy()
        if self.height < 0:  # water
            self.color = lerp_color((51, 153, 255), (0, 105, 148), limit(-self.height * 2.5, 0, 1))
            self.image = sprite_dict["water"]
        elif self.height < 0.45:  # land
            self.color = (0, 190, 0)
            self.walkable = True
            self.image = sprite_dict["grass"]
        elif self.height < 0.7:  # grey mountain
            self.color = format_color(120 * (1 - (self.height - 0.4) / 0.25 / 4))
            self.walkable = True
            self.image = sprite_dict["hills"]
        else:  # snow
            self.color = (255, 255, 255)  # lerp_color((175, 175, 175), (255, 255, 255), (self.height - 0.65) / 0.1)
            self.image = sprite_dict["mountain" if random.choices([True, False]) else "SmallerMountain"]

        if self.height < 0:
            self.pos = self.pos + 1

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.isWater = self.height < 0
        # if self.isWater:
        #     self.points = self.points + 2

    def init(self, tiles, fieldSize):
        pass
        # if self.y > 0: self.bordering_tiles.append(tiles[int(self.x)][int(self.y - 1)])
        # if self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x)][int(self.y + 1)])
        # if self.x > 0: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y)])
        # if self.x < fieldSize[0] - 1: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y)])
        # if self.x % 2 == 0:
        #     if self.x > 0 and self.y > 0: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y - 1)])
        #     if self.x < fieldSize[0] - 1 and self.y > 0: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y - 1)])
        # else:
        #     if self.x > 0 and self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y + 1)])
        #     if self.x < fieldSize[0] - 1 and self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y + 1)])

    # def display(self):
    #     if self.isWater:
    #         self.screen.aapolygon(self.points, self.color)  # , stroke_color=self.stroke_color)
    #     else:
    #         self.screen.aapolygon(self.points, self.color, stroke_color=self.stroke_color)
    #
    # def higlight(self):
    #     self.screen.aapolygon(self.points, (int(limit(self.color[0] * 2, 0, 255)), int(limit(self.color[1] * 2, 0, 255)),
    #                                         int(limit(self.color[2] * 2, 0, 255))), stroke_color=self.stroke_color)
    #
    # def debug(self, mouse):
    #     if math.dist(mouse, self.pos) <= self.size * 0.5:
    #         self.higlight()
    #         # for tile in self.bordering_tiles:
    #         #     tile.higlight()

    def is_walkable(self):
        return self.walkable

    def __lt__(self, other):
        return self.pos[1] < other.pos[1]
        # return math.dist(self.pos, (0, 0)) < math.dist(other.pos, (0, 0))


def limit(value, min, max):
    if value < min:
        value = min
    elif value > max:
        value = max

    return value
