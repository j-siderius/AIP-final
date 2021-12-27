import copy
import random

import numpy as np

import Screen
from Screen import *
from perlin_noise import PerlinNoise
import math
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, place, size, radius, points, screen: Screen, noise: PerlinNoise, resource_noise: PerlinNoise, sprite_dict: dict, field):
        super().__init__()
        self.field = field
        self.screen = screen
        self.size = size
        self.radius = radius
        self.pos = np.array(pos)
        self.x = place[0]
        self.y = place[1]
        self.bordering_tiles = []

        self.walkable = False
        self.walkspeed = 0
        self.is_wall = False
        self.hitpoints = 0

        self.sprite_dict = sprite_dict
        self.index_of_sprite = None
        self.image_name = ""
        self.is_highlight = False
        self.is_selected = False

        self.color = (0, 100, 0)
        self.stroke_color = (110, 110, 110)

        self.height = noise([self.pos[0] / 300, self.pos[1] / 300]) * 1.5
        self.resource_value = resource_noise([self.pos[0]/300, self.pos[1]/300])

        # make the height drop off at the edges:
        width, height = self.screen.get_size()
        dist_center_x = abs(width / 2 - self.pos[0])
        dist_center_y = abs(height / 2 - self.pos[1])
        self.height -= (dist_center_x ** 2) / ((width * 0.5) ** 2) - 0.2
        self.height -= (dist_center_y ** 2) / ((height * 0.6) ** 2) - 0.2

        if (pos[1] < size[1] or pos[1] > screen.get_height() - size[1]) and self.height > 0:
            self.height -= 0.2
            if self.height > 0: self.height = -0.1

        if self.height < 0:  # water
            self.index_of_sprite = limit(round(-self.height * (7 + Settings.WATER_DROP_OFF_SCALING*4)), 0, 7)
            self.image_name = "water"
        elif self.height < 0.45:  # land
            self.walkable = True
            self.image_name = "grass"
            self.walkspeed = 1
        elif self.height < 0.7:  # grey mountain
            self.walkable = True
            self.image_name = "hills"
            self.walkspeed = 0.5
        else:  # snow
            self.image_name = "mountain"

        self.is_water = self.height < 0

        self.resource: ResourceTiles = ResourceTiles.none
        if self.is_water:
            self.pos = self.pos + 1
        elif self.is_walkable():
            # resources:
            if self.resource_value > 0.05:
                if "hills" in self.image_name or self.resource_value < 0.2:
                    self.image_name = f"forest_{self.image_name}"
                    self.resource = ResourceTiles.forest
                else:
                    self.image_name = f"large_forest_{self.image_name}"
                    self.resource = ResourceTiles.large_forest
                    self.walkspeed = 0.5

        self.coastal_tile = False

        if self.image_name in self.sprite_dict.keys() and isinstance(self.sprite_dict[self.image_name], list) and self.index_of_sprite is None:
            self.index_of_sprite = random.randint(0, len(sprite_dict[self.image_name]) - 1)

        self.change_image(self.image_name)
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

        for tile in self.bordering_tiles:
            if self.pos[1] > tile.pos[1] and tile.is_water:
                self.coastal_tile = True

    def update(self, mouse):
        if self.isOver(mouse) and self.is_highlight and not self.is_selected:
            self.is_selected = True
            self.highlight()
        elif not self.isOver(mouse) and self.is_highlight and self.is_selected:
            self.is_selected = False
            self.change_image(self.image_name)

    def update_Tile(self):
        if self.is_highlight:
            self.highlight()

    def highlight(self, color=Settings.HIGHLIGHT_COLOR):
        if self.is_selected and color == Settings.HIGHLIGHT_COLOR:  # when the mouse is over it, make it a different color
            color = Settings.HIGHLIGHT_COLOR_SELECTED
        if self.is_wall and color == Settings.HIGHLIGHT_COLOR:  # show the action icon when the user can only do an action
            color = Settings.HIGHLIGHT_COLOR_ACTION
        elif (not self.is_wall and not self.walkable) or self.is_water:  # don't show an action when the user can't do an action
            return

        color = format_color(color)
        self.is_highlight = True
        # self.change_image(self.image_name, False)
        self.image = self.image.copy()
        # self.image.blit(self.sprite_dict["is_highlight"], (0, 0))
        draw.filled_circle(self.image, round(self.size[0] / 2), round(self.image.get_height() - self.size[1] / 2 - 3), int(self.radius * 0.5), color)

    def unhighlight(self):
        self.is_highlight = False
        self.change_image(self.image_name)

    def has_resources(self):
        return self.resource != ResourceTiles.none

    def can_build(self):
        return self.is_walkable()

    def has_structure(self):
        return self.is_wall

    def build_wall(self):
        self.hitpoints = 100
        self.is_wall = True
        self.image_name = f"wall_{self.image_name}"
        self.change_image(self.image_name)

    def destroy_structure(self):
        if self.is_wall:
            self.hitpoints = 0
            self.is_wall = False
            self.image_name = self.image_name.replace("wall_", "")
            self.change_image(f"{self.image_name}")

            if self.coastal_tile:
                self.field.update_coastal_waters()

    def mine_resource(self):
        resource = None
        if self.resource == ResourceTiles.forest:
            self.resource = ResourceTiles.none
            resource = Resources.wood
            self.image_name = self.image_name.replace("forest_", "")
            self.change_image(self.image_name)

        elif self.resource == ResourceTiles.large_forest:
            self.resource = ResourceTiles.forest
            resource = Resources.wood
            self.image_name = self.image_name.replace("large_", "")

            if "hills" not in self.image_name:
                self.walkspeed = 1
            self.change_image(f"{self.image_name}")

        if resource and self.coastal_tile:
            self.field.update_coastal_waters()

        return resource

    def change_image(self, image_name, update_tile=True):
        if isinstance(self.sprite_dict[image_name], list):
            self.image = self.sprite_dict[image_name][self.index_of_sprite]#.copy()
        else:
            self.image = self.sprite_dict[image_name]#.copy()

        if update_tile:
            self.update_Tile()

    def isOver(self, point):
        return math.dist(point, self.hex_rect.center) <= self.radius

    # returns the walkspeed if a tile is walkable, otherwise return False
    def is_walkable(self):
        if self.walkable and not self.is_wall:
            return self.walkspeed
        else: return False

    def highlight_neighbours(self):
        for tile in self.bordering_tiles:
            tile.highlight()

    def unhighlight_neighbours(self):
        for tile in self.bordering_tiles:
            tile.unhighlight()

    def get_neighbours(self):
        return self.bordering_tiles

    def get_points(self):
        return self.points

    def get_center(self):
        return self.hex_rect.center

    def get_bottomleft(self):
        return self.hex_rect.bottomleft

    def __lt__(self, other):
        return self.pos[1] < other.pos[1]


def limit(value, min, max):
    if value < min:
        value = min
    elif value > max:
        value = max

    return value
