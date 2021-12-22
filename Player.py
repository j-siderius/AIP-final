import random
import pygame
from Field import Field
import helper

# TODO
#   - add break timer, so like it cost time to break something (prob do it with the cursor highlight thingy)
#   - walk niet meer teleporteren maken, maar dat die echt loopt.


class Player:

    def __init__(self, screen, field_size, field: Field):
        self.screen = screen
        self.field = field
        hex_amount = field.field_size

        self.field_size = field_size

        self.x, self.y = None, None
        self.xPos, self.yPos = 0, 0
        self.radius = self.field.hex_size / 2.3  # base this on hex_size of Tiles
        # assign starting position to a viable tile
        self.find_starting_tile(int(hex_amount[0] / 2), int(hex_amount[1] / 2))

        self.inventory = dict()

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

    # def update(self):
    #     self.player_input(self.screen.get_mouse_pos(), self.screen.get_mouse_pressed(), self.screen.get_pressed_keys())

    def mouse_pressed(self, mousePos, button):
        if button == 1:
            pressed_tile = self.field.get_tile_from_point(mousePos)
            self.move_player(pressed_tile.x, pressed_tile.y)
        elif button == 3:
            pressed_tile = self.field.get_tile_from_point(mousePos)

            if pressed_tile in self.field.get_tile(self.xPos, self.yPos).bordering_tiles:
                resource = pressed_tile.mine_resource()
                if resource is not None:
                    if resource in self.inventory:
                        self.inventory[resource] += 1
                    else:
                        self.inventory[resource] = 1

    def move_player(self, targetTileX, targetTileY):
        neighbours = self.field.get_tile(self.xPos, self.yPos).bordering_tiles
        for neighbour in neighbours:
            if (neighbour.x, neighbour.y) == (targetTileX, targetTileY) and self.field.get_tile(targetTileX, targetTileY).walkable:
                # TODO: implement tick rate with something like nextTile = this.tile
                self.align_player(targetTileX, targetTileY)

    # employ walking algorithm to find suitable starting tile
    def find_starting_tile(self, tileX, tileY):
        tile = self.field.get_tile(tileX, tileY)
        if tile.is_walkable() != 1:
            try_tile = tile.bordering_tiles[random.randint(0, len(tile.bordering_tiles) - 1)]
            self.find_starting_tile(try_tile.x, try_tile.y)
        else:
            # assign player position to the found grass tile
            print(f"Starting tile found: ({tileX},{tileY})")
            hex_size = self.field.get_hex_size()
            self.align_player(tileX, tileY)

    def align_player(self, x, y):
        self.xPos = x
        self.yPos = y
        self.x, self.y = self.field.get_tile(x, y).get_center()
