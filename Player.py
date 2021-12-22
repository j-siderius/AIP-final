import random
import pygame

import Tile
from Field import Field
from settings import *
from Screen import *
import helper

# TODO
#   - add break timer, so like it cost time to break something (prob do it with the cursor highlight thingy)


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

        # walking
        self.is_walking = False
        self.walk_timer = 0
        self.from_tile = self.current_tile
        self.target_tile = None

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
        # if len(menu_txt) == 1:
        #     menu_txt.append("Empty")
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
            else:
                self.x, self.y = lerp_2D(self.from_tile.get_center(), self.target_tile.get_center(), factor)

    def mouse_pressed(self, mousePos, button):
        if button == MouseButton.left and not self.is_walking:
            pressed_tile = self.field.get_tile_from_point(mousePos)
            self.move_player(pressed_tile.x, pressed_tile.y)

        elif button == MouseButton.right and not self.is_walking:  # right mouse button
            pressed_tile = self.field.get_tile_from_point(mousePos)

            if pressed_tile in self.current_tile.get_neighbours():
                # resource mining
                if pressed_tile.has_resources():
                    resource = pressed_tile.mine_resource()
                    if resource is not None:
                        if resource in self.inventory:
                            self.inventory[resource] += 1
                        else:
                            self.inventory[resource] = 1

                elif pressed_tile.can_build():  # building
                    # wooden wall
                    if self.inventory[Resources.wood] >= Settings.WOODEN_WALL_COST:
                        self.inventory[Resources.wood] -= Settings.WOODEN_WALL_COST
                        pressed_tile.build_wall()
                elif pressed_tile.has_structure():
                    pressed_tile.destroy_structure()

    def move_player(self, targetTileX, targetTileY):
        neighbours = self.current_tile.get_neighbours()
        for neighbour in neighbours:
            if (neighbour.x, neighbour.y) == (targetTileX, targetTileY) and self.field.get_tile(targetTileX, targetTileY).is_walkable():
                # TODO: implement tick rate with something like nextTile = this.tile
                self.is_walking = True
                self.walk_timer = Settings.PLAYER_WALKING_TIME
                self.target_tile = neighbour

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
