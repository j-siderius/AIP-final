import numpy as np
from Screen import *
# import noise
from perlin_noise import PerlinNoise
import math


class Tile:
    def __init__(self, pos, place, size, points, screen: Screen, noise: PerlinNoise):
        self.screen = screen
        self.size = size
        self.pos = np.array(pos)
        self.x = place[0]
        self.y = place[1]
        self.bordering_tiles = []

        self.color = (0, 100, 0)
        self.points = np.array(points) + pos
        self.stroke_color = (110)


        # self.height = noise.pnoise2(self.pos[0] / 300 + 500, self.pos[1] / 300 + 450, 1, 0.1) + noise.pnoise2(self.pos[0] / 300 + 1000, self.pos[1] / 300, 1, 0.1)/2
        self.height = noise([self.pos[0] / 300 + 500, self.pos[1] / 300 + 450]) * 1.5
        print(self.height)
        # dist_to_center = math.dist(pos, (screen.get_width() / 2, screen.get_height() / 2))
        # max_dist_to_center = math.dist((0, 0), (screen.get_width() / 2, screen.get_height() / 2))

        # self.height += limit((max_dist_to_center*0.5 - dist_to_center) / (max_dist_to_center*0.5) + 0.5, 0.5, 1) - 0.5
        # self.height = (self.height + 1) * limit((max_dist_to_center - dist_to_center) / (max_dist_to_center * 0.3), 0, 1.5) - 1

        # if dist_to_center > max_dist_to_center * 0.6:
        #     if self.height < 0.1: self.height = -1
        #     self.height *= limit(abs(2-(dist_to_center - max_dist_to_center) / max_dist_to_center) * 2, 0, 1)

        if self.height > 0.1:
            pass
            # self.height += abs(noise.snoise2(self.pos[0] / 100, self.pos[1] / 100, 1, 0.1) * 0.02)
            # self.height += abs(noise.pnoise2(self.pos[0] / 100+ 1000, self.pos[1] / 100, 1, 0.1) * 0.3)

        if self.height < -0.1:
            self.color = lerp_color((51, 153, 255), (0, 105, 148), limit(-self.height * 2.5, 0, 1))
        # elif self.height < 0.05:
        #     self.color = (254, 220, 100)  # lerp_color((51, 153, 255), (254, 220, 100), limit((self.height + 0.1) / 0.15 + 0.3, 0, 1))#(0.15 - self.height - 0.1)/0.15)
        elif self.height < 0.35:
            self.color = (0, 190, 0)  # (0, 255 * limit(1 - self.height, 0, 1), 0)
        elif self.height < 0.55:
            self.color = Screen.format_color(120 * (1-(self.height - 0.35)/0.20/4))  # lerp_color((0, 255 * limit(1 - self.height, 0, 1), 0), (120, 120, 120), (self.height - 0.2) / 0.3) #255 * (self.height - 0.5) / 0.5
        else:
            self.color = lerp_color((175, 175, 175), (255, 255, 255), (self.height - 0.5) / 0.1)

        self.isWater = self.height < -0.1
        if self.isWater:
            self.points = self.points + 2

    def init(self, tiles, fieldSize):
        if self.y > 0: self.bordering_tiles.append(tiles[int(self.x)][int(self.y - 1)])
        if self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x)][int(self.y + 1)])
        if self.x > 0: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y)])
        if self.x < fieldSize[0] - 1: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y)])
        if self.x % 2 == 0:
            if self.x > 0 and self.y > 0: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y - 1)])
            if self.x < fieldSize[0]-1 and self.y > 0: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y - 1)])
        else:
            if self.x > 0 and self.y < fieldSize[1]-1: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y + 1)])
            if self.x < fieldSize[0]-1 and self.y < fieldSize[1]-1: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y + 1)])

    def display(self, highlight=False):
        if highlight:
            self.screen.aapolygon(self.points, (int(limit(self.color[0]*2, 0, 255)), int(limit(self.color[1]*2, 0, 255)), int(limit(self.color[2]*2, 0, 255))),
                                  stroke_color=self.stroke_color)
            return

        if self.isWater:
            self.screen.aapolygon(self.points, self.color)  # , stroke_color=self.stroke_color)
        else:
            self.screen.aapolygon(self.points, self.color, stroke_color=self.stroke_color)

    def debug(self, mouse):
        if math.dist(self.screen.get_mouse_pos(), self.pos) <= self.size/2:
            for tile in self.bordering_tiles:
                tile.display(True)
            print(len(self.bordering_tiles))


def limit(value, min, max):
    if value < min:
        value = min
    elif value > max:
        value = max

    return value
