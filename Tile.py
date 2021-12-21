import copy
import random

import numpy as np
from Screen import *
# import noise
from perlin_noise import PerlinNoise
import math
from enum import Enum


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, place, size, radius, points, screen: Screen, noise: PerlinNoise, resource_noise: PerlinNoise, sprite_dict: dict):
        super().__init__()
        self.screen = screen
        self.size = size
        self.radius = radius
        self.pos = np.array(pos)
        self.x = place[0]
        self.y = place[1]
        self.bordering_tiles = []
        self.walkable = False
        self.walkspeed = 0

        self.sprite_dict = sprite_dict
        self.image_name = ""
        self.highlight = False

        self.color = (0, 100, 0)
        self.stroke_color = (110, 110, 110)

        self.height = noise([self.pos[0] / 300, self.pos[1] / 300]) * 1.5
        self.resource_value = resource_noise([self.pos[0]/300, self.pos[1]/300])
        print(self.resource_value)

        # make the height drop off at the edges:
        width, height = self.screen.get_size()
        dist_center_x = abs(width / 2 - self.pos[0])
        dist_center_y = abs(height / 2 - self.pos[1])
        self.height -= (dist_center_x ** 2) / ((width * 0.5) ** 2) - 0.2
        self.height -= (dist_center_y ** 2) / ((height * 0.6) ** 2) - 0.2

        if (pos[1] < size[1] or pos[1] > screen.get_height() - size[1]) and self.height > 0:
            self.height -= 0.2
            if self.height > 0: self.height = -1

        if self.height < 0:  # water
            self.color = lerp_color((51, 153, 255), (0, 105, 148), limit(-self.height * 2.5, 0, 1))
            self.image = sprite_dict["water"]
        elif self.height < 0.45:  # land
            self.color = (0, 190, 0)
            self.walkable = True
            self.image = sprite_dict["grass"]
            self.image_name = "grass"
            self.walkspeed = 1
        elif self.height < 0.7:  # grey mountain
            self.color = format_color(120 * (1 - (self.height - 0.4) / 0.25 / 4))
            self.walkable = True
            self.index_of_sprite = random.randint(0, len(sprite_dict["hills"])-1)
            self.image = sprite_dict["hills"][self.index_of_sprite]
            self.image_name = "hills"
            self.walkspeed = 0.5
        else:  # snow
            self.color = (255, 255, 255)  # lerp_color((175, 175, 175), (255, 255, 255), (self.height - 0.65) / 0.1)
            self.image = sprite_dict["mountain" if random.choices([True, False]) else "SmallerMountain"]

        self.isWater = self.height < 0

        self.resource: Resource = Resource.none
        if self.isWater:
            self.pos = self.pos + 1
        elif self.is_walkable():
            # resources:
            if self.resource_value > 0.2: #large forest
                self.resource = Resource.large_forest
                if self.image_name == "hills":
                    self.image_name = "large_foresthills"
                    self.image = sprite_dict[self.image_name]
                else:
                    self.image_name = "large_forest"
                    self.image = sprite_dict[self.image_name]
                    self.walkspeed = 0.5
            elif self.resource_value > 0.05:
                self.resource = Resource.forest
                if self.image_name == "hills":
                    self.image_name = "foresthills"
                    self.image = sprite_dict[self.image_name]
                else:
                    self.image_name = "forest"
                    self.image = sprite_dict[self.image_name]

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.hex_rect = pygame.Rect((0, 0), size)  # (self.rect.bottomleft - np.array([-size[0]/2, -size[1]/2])), size)
        self.hex_rect.bottomleft = self.rect.bottomleft
        self.hex_rect.move_ip(0, -3)

        # points are arranged in the following manner: [0]=bottom-right, [1]=bottom-left, [2]=middle-left, [3]=top-left, [4]=top-right,
        # [5]=middle-right. aka, starting right and then clockwise.
        self.points = np.array(points) + self.hex_rect.center + np.array([0, -2])

    def init(self, tiles, fieldSize):
        if self.y > 0: self.bordering_tiles.append(tiles[int(self.x)][int(self.y - 1)])
        if self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x)][int(self.y + 1)])
        if self.x > 0: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y)])
        if self.x < fieldSize[0] - 1: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y)])
        if self.x % 2 == 0:
            if self.x > 0 and self.y > 0: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y - 1)])
            if self.x < fieldSize[0] - 1 and self.y > 0: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y - 1)])
        else:
            if self.x > 0 and self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y + 1)])
            if self.x < fieldSize[0] - 1 and self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y + 1)])

    def display(self):
        if self.isWater:
            self.screen.aapolygon(self.points, self.color)  # , stroke_color=self.stroke_color)
        # else:
        #     self.screen.aapolygon(self.points, self.color, stroke_color=self.stroke_color)

    def higlight(self, color=(255,100)):
        self.screen.aapolygon(self.points, color, stroke_color=self.stroke_color)

    def update(self, mouse):
        # TODO make a selection img of the new hills2
        if self.isOver(mouse) and self.is_walkable() and not self.highlight:
            self.highlight = True
            self.image = self.sprite_dict[f"selected_{self.image_name}"]
        elif not self.isOver(mouse) and self.highlight:
            self.highlight = False
            if isinstance(self.sprite_dict[self.image_name], list):
                self.image = self.sprite_dict[self.image_name][self.index_of_sprite]
            else:
                self.image = self.sprite_dict[self.image_name]

    # TEMP
    def mouse_pointer(self, mouse):
        if self.isOver(mouse) and not self.isWater:
            self.higlight()

    def isOver(self, point):
        return math.dist(point, self.hex_rect.center) <= self.radius

    # returns the walkspeed if a tile is walkable, otherwise return False
    def is_walkable(self):
        if self.walkable:
            return self.walkspeed
        else: return False

    def get_points(self):
        return self.points

    def get_center(self):
        return self.hex_rect.center

    def get_bottomleft(self):
        return self.hex_rect.bottomleft

    def __lt__(self, other):
        return self.pos[1] < other.pos[1]
        # return math.dist(self.pos, (0, 0)) < math.dist(other.pos, (0, 0))


def limit(value, min, max):
    if value < min:
        value = min
    elif value > max:
        value = max

    return value


class Resource(Enum):
    none = -1
    forest = 0
    large_forest = 1
    rock = 2
    large_rock = 3
