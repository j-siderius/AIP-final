import random

import Screen
from Screen import *
from perlin_noise import PerlinNoise
import math
from Data.settings import *
from Data.TilesData import *


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

        self.is_wall = False
        self.hitpoints = 0

        self.sprite_dict = sprite_dict
        self.index_of_sprite = None
        self.image_name = ""
        self.is_highlight = False
        self.is_selected = False

        # noise for the terrain and resource generation
        self.height = noise([self.pos[0] / 300, self.pos[1] / 300]) * 1.5
        self.resource_value = resource_noise([self.pos[0] / 300, self.pos[1] / 300])

        # make the terrain height drop off at the edges, so it becomes an island
        width, height = self.screen.get_size()
        dist_center_x = abs(width / 2 - self.pos[0])
        dist_center_y = abs(height / 2 - self.pos[1])
        self.height -= (dist_center_x ** 2) / ((width * 0.5) ** 2) - 0.2
        self.height -= (dist_center_y ** 2) / ((height * 0.6) ** 2) - 0.2

        if (pos[1] < size[1] or pos[1] > screen.get_height() - size[1]) and self.height > 0:
            self.height -= 0.2
            if self.height > 0:
                self.height = -0.1

        # initialize the tile sprites
        if self.height < 0:  # water
            self.index_of_sprite = limit(round(-self.height * (7 + Settings.WATER_DROP_OFF_SCALING * 4)), 0, 7)
            self.image_name = "water"
        elif self.height < 0.45:  # land
            self.image_name = "grass"
        elif self.height < 0.7:  # grey mountain
            self.image_name = "hills"
        else:  # snow
            self.image_name = "mountain"

        self.is_water = self.height < 0

        # setup the tile properties temporarily to see were resources can spawn
        self.tile_property: TileProperty = tiles_dict[self.image_name]

        # self.tile_property.resource: ResourceTiles = ResourceTiles.none
        if self.is_water:
            self.pos = self.pos + 1
        elif self.is_walkable():
            # resources:
            if self.resource_value > 0.05:
                if "hills" in self.image_name or self.resource_value < 0.2:
                    self.image_name = f"forest_{self.image_name}"
                else:
                    self.image_name = f"large_forest_{self.image_name}"

            # setup the tile properties
            self.tile_property: TileProperty = tiles_dict[self.image_name]

        # setup the action variables
        self.current_action_time = self.tile_property.action_time
        self.current_action = ActionType.none
        self.end_action_func = None
        self.coastal_tile = False

        # if there are multiple sprites for the given tile and the index of the sprite hasn't been determined yet, choose a random index
        if self.image_name in self.sprite_dict.keys() and isinstance(self.sprite_dict[self.image_name], list) and self.index_of_sprite is None:
            self.index_of_sprite = random.randint(0, len(sprite_dict[self.image_name]) - 1)

        # setup the sprite
        self.change_image(self.image_name)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # setup the rectangle over the actual hexagon instead of the sprite.
        self.hex_rect = pygame.Rect((0, 0), size)
        self.hex_rect.bottomleft = self.rect.bottomleft
        self.hex_rect.move_ip(0, -3)

        # points are arranged in the following manner: [0]=bottom-right, [1]=bottom-left, [2]=middle-left, [3]=top-left, [4]=top-right,
        # [5]=middle-right. aka, starting right and then clockwise.
        self.points = np.array(points) + self.hex_rect.center + np.array([0, -2])

    def init(self, tiles, fieldSize):
        # find the bordering tiles:
        if self.y > 0: self.bordering_tiles.append(tiles[int(self.x)][int(self.y - 1)])  # Top
        if self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x)][int(self.y + 1)])  # bottom
        if self.x > 0: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y)])  # left
        if self.x < fieldSize[0] - 1: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y)])  # right
        if self.x % 2 == 0:
            if self.x > 0 and self.y > 0: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y - 1)])  # left top
            if self.x < fieldSize[0] - 1 and self.y > 0: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y - 1)])
        else:
            if self.x > 0 and self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x - 1)][int(self.y + 1)])
            if self.x < fieldSize[0] - 1 and self.y < fieldSize[1] - 1: self.bordering_tiles.append(tiles[int(self.x + 1)][int(self.y + 1)])

        for tile in self.bordering_tiles:
            if self.pos[1] > tile.pos[1] and tile.is_water:
                self.coastal_tile = True

    def update(self, mouse):  # update called in field
        # if an action is happening on this tile
        if self.current_action != ActionType.none:
            if self.is_selected:  # if the user is breaking thing type show a little animation
                self.highlight()
            self.current_action_time -= self.screen.get_elapsed_time()

            # if the action is finished
            if self.current_action_time <= 0:
                self.end_action()

        # if the wall is broken by an enemy
        if self.is_wall and self.hitpoints < 0:
            self.destroy_structure()

    def update_Tile(self):  # internal update of the tile
        # highlight the tiles around the player to show the options
        if self.is_highlight:
            self.highlight()

    def select_tile(self):
        self.is_selected = True
        self.highlight()

    def unselect_tile(self):
        self.is_selected = False
        self.change_image(self.image_name)

    # a generic highlight function to highlight the tile by drawing a colored circle in the middle of it
    def highlight(self, color=Settings.HIGHLIGHT_COLOR):  # highlight the tiles around the player to show the options
        if self.is_selected and color == Settings.HIGHLIGHT_COLOR:  # when the mouse is over it, make it a different color
            color = Settings.HIGHLIGHT_COLOR_SELECTED
        if self.is_wall and color == Settings.HIGHLIGHT_COLOR:  # show the action icon when the user can only do an action
            color = Settings.HIGHLIGHT_COLOR_ACTION
        elif (not self.is_wall and not self.tile_property.walkable) or self.is_water:  # don't show an action when the user can't do an action
            return

        # if an action is happening, change the circle to reflect it
        if self.current_action_time != self.tile_property.action_time and self.tile_property.action_time != 0:
            color = lerp_color(color, (255, 0, 0), 1 - self.current_action_time / self.tile_property.action_time)

        # draw a colored circle to highlight the tile
        color = format_color(color)
        self.is_highlight = True
        self.image = self.image.copy()

        draw.filled_circle(self.image, round(self.size[0] / 2), round(self.image.get_height() - self.size[1] / 2 - 3), int(self.radius * 0.5), color)

    def unhighlight(self):  # remove the highlight from the tile
        self.is_highlight = False
        self.change_image(self.image_name)

    def has_resources(self):
        return self.tile_property.resource_tile != ResourceTiles.none

    def can_build(self):
        return self.is_walkable()

    def has_structure(self):
        return self.is_wall

    # the 'public' action that the player calls
    def action_build_wall(self, end_action_func):
        self.end_action_func = end_action_func
        self.current_action = ActionType.building
        self.current_action_time = self.tile_property.action_time

    # the actual building of the wall, called when action is finished
    def build_wall(self):
        self.is_wall = True
        self.image_name = f"wall_{self.image_name}"
        self.change_image(self.image_name)
        self.hitpoints = self.tile_property.hitpoints

    # the 'public' action that the player calls
    def action_destroy_structure(self, end_action_func):
        self.end_action_func = end_action_func
        self.current_action = ActionType.destroying
        self.current_action_time = self.tile_property.action_time

    # the actual destroying of the structure (wall), called when action is finished
    def destroy_structure(self):
        resource, amount = self.tile_property.resource, self.tile_property.resource_amount

        self.is_wall = False
        self.image_name = self.image_name.replace("wall_", "")
        self.change_image(f"{self.image_name}")

        # if the tile is next to the water redraw/update the water tiles
        if self.coastal_tile:
            self.field.update_water()

        return resource, amount

    # the 'public' action that the player calls
    def action_mine_resource(self, end_action_func):
        self.end_action_func = end_action_func
        self.current_action = ActionType.mining
        self.current_action_time = self.tile_property.action_time

    # the actual mining of the resource (forest), called when action is finished
    def mine_resource(self):
        resource = None
        amount = 0
        if self.tile_property.resource_tile == ResourceTiles.forest:
            resource = self.tile_property.resource
            self.image_name = self.image_name.replace("forest_", "")
            self.change_image(self.image_name)

        elif self.tile_property.resource_tile == ResourceTiles.large_forest:
            resource = self.tile_property.resource
            self.image_name = self.image_name.replace("large_", "")
            self.change_image(f"{self.image_name}")

        if resource and self.coastal_tile:
            self.field.update_water()

        if resource:
            amount = self.tile_property.resource_amount

        return resource, amount

    # called when the action is finished, calls the separate action functions
    def end_action(self):
        if self.current_action == ActionType.mining:
            resource, amount = self.mine_resource()
            self.end_action_func(resource, amount)
        if self.current_action == ActionType.building:
            self.build_wall()
            self.end_action_func(None, 0)
        if self.current_action == ActionType.destroying:
            resource, amount = self.destroy_structure()
            print(resource, amount)
            self.end_action_func(resource, amount)

        self.current_action_time = self.tile_property.action_time
        self.current_action = ActionType.none
        self.highlight()  # reset the highlight

    # changes the kind of tile it is, aka the sprite/image
    def change_image(self, image_name, update_tile=True):
        # find the new sprite in the sprite dict
        if isinstance(self.sprite_dict[image_name], list):
            self.image = self.sprite_dict[image_name][self.index_of_sprite]
        else:
            self.image = self.sprite_dict[image_name]

        # set the new sprite properties
        self.tile_property: TileProperty = tiles_dict[self.image_name]

        if update_tile:
            self.update_Tile()

    def isOver(self, point):
        return math.dist(point, self.hex_rect.center) <= self.radius

    # returns the walkspeed if a tile is walkable, otherwise return False
    def is_walkable(self):
        if self.tile_property.walkable and not self.is_wall:
            return self.tile_property.walkspeed
        else:
            return False

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

    def get_position(self):
        return [self.x, self.y]

    def __lt__(self, other):
        return self.pos[1] < other.pos[1]


class ActionType(Enum):
    none = 0
    mining = 1
    building = 2
    destroying = 3


def limit(value, min, max):
    if value < min:
        value = min
    elif value > max:
        value = max

    return value
