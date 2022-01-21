import random
import pygame
import math

import Tile
from Field import Field
from Data.settings import *
from Screen import *


class Player:

    def __init__(self, screen, field_size, field: Field):
        self.screen = screen
        self.field = field
        hex_amount = field.field_size

        self.field_size = field_size

        self.x, self.y = None, None  # pos on the world map
        self.current_tile: Tile = None
        self.radius = self.field.hex_size / 2.3  # base this on hex_size of Tiles
        # assign starting position to a viable tile
        self.find_starting_tile(int(hex_amount[0] / 2), int(hex_amount[1] / 2))
        # is_highlight the next moves
        self.current_tile.highlight_neighbours()

        # walking
        self.is_walking = False
        self.walk_timer = 0
        self.from_tile = self.current_tile
        self.target_tile = None

        # mining and building
        # self.last_mouse_down_time = 0
        self.doing_an_action = False
        self.inventory = {Resources.wood: 100}  # dict()

        self.color = (255, 0, 0)

    def display(self):
        self.screen.stroke_size(0)
        self.screen.stroke(self.color)
        self.screen.circle(self.x, self.y, self.radius, self.color)

        # inventory menu
        menu_txt = ["Inventory: "]
        for key, value in self.inventory.items():
            menu_txt.append(f"{key}: {value}")

        self.screen.text_font(25)
        width, height = self.screen.get_size()
        self.screen.text_array(width - 110, 20, menu_txt, 255, background_color=0)

    def update(self):
        if self.is_walking:  # walking
            factor = 1 - self.walk_timer / Settings.PLAYER_WALKING_TIME
            walkspeed = lerp(self.current_tile.is_walkable(), self.target_tile.is_walkable(), factor)
            self.walk_timer -= self.screen.get_elapsed_time() * walkspeed
            if self.walk_timer <= 0:
                self.is_walking = False
                self.align_player(self.target_tile)
                self.from_tile = self.current_tile

                # is_highlight the next moves
                self.current_tile.highlight_neighbours()
            else:
                self.x, self.y = lerp_2D(self.from_tile.get_center(), self.target_tile.get_center(), factor)

    def move_player(self, targetTile):
        """Moves the player to the clicked tile (if valid move)"""
        if self.is_walking or self.doing_an_action:
            return

        targetTileX = targetTile[0]
        targetTileY = targetTile[1]
        neighbours = self.current_tile.get_neighbours()
        for neighbour in neighbours:
            neighbour.unselect_tile()
            if (neighbour.x, neighbour.y) == (targetTileX, targetTileY) and self.field.get_tile(targetTileX, targetTileY).is_walkable():
                # TODO: implement tick rate with something like nextTile = this.tile
                self.current_tile.unhighlight_neighbours()
                self.is_walking = True
                self.walk_timer = Settings.PLAYER_WALKING_TIME
                self.target_tile = neighbour

    def mine_build(self, pressed_tile):
        """Performs the player action on the clicked tile (mine, build, destroy)"""
        if self.is_walking or self.doing_an_action:
            return

        # resource mining
        if pressed_tile.has_resources():  # if the tile has resources
            pressed_tile.action_mine_resource(self.end_action)

        # building
        elif pressed_tile.can_build():
            # wooden wall
            if self.inventory[Resources.wood] >= Settings.WOODEN_WALL_COST:
                pressed_tile.action_build_wall(self.end_action)
                self.inventory[Resources.wood] -= Settings.WOODEN_WALL_COST

        # destroying buildings
        elif pressed_tile.has_structure():
            pressed_tile.action_destroy_structure(self.end_action)

    # employ walking algorithm to find suitable starting tile
    def find_starting_tile(self, tileX, tileY):
        tile = self.field.get_tile(tileX, tileY)
        if tile.is_walkable() != 1:
            try_tile = tile.get_neighbours()[random.randint(0, len(tile.get_neighbours()) - 1)]
            self.find_starting_tile(try_tile.x, try_tile.y)
        else:
            # assign player position to the found grass tile
            print(f"Starting tile found: ({tileX},{tileY})")
            self.align_player(tile)

    def align_player(self, tile: Tile):
        self.current_tile = tile
        self.x, self.y = tile.get_center()

    # called when the player starts an action, not called when the player moves
    def start_action(self):
        # TODO !!!! @JANNICK set here your time tick thingy, deze is called when an action is started !!!!!!!
        self.doing_an_action = True

    def end_action(self, gained_resource, amount):
        if gained_resource is not None:  # if a resource was gained in the action
            if gained_resource in self.inventory:  # if the user already has a resource then just add it.
                self.inventory[gained_resource] += amount
            else:  # if the user doesn't than add the resource to the inventory
                self.inventory[gained_resource] = amount

        # set doing an action to false so the user can start another action
        self.doing_an_action = False

    def get_player_position(self):
        return (self.x, self.y)

    def get_current_tile(self):
        return self.current_tile

    def set_resource(self, resource):
        if resource is not None:
            if resource in self.inventory:
                self.inventory[resource] += 1
            else:
                self.inventory[resource] = 1
        pass

