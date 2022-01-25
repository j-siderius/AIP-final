import math
from Data.settings import *
from Player import *
import time


class Input:
    def __init__(self, player):
        """
        Processes all the different inputs into usable variables
        :param player: pass the main player object here:
        """
        self.selected_tile = 5
        self.prev_selected_tile = -1
        self.player = player
        self.elapsed_time = 0
        self.old_time = time.perf_counter()

    def process_nunchuck_movement(self, joystick):
        """
        Processes the movement data from the connected controller
        :param joystick: [JoyX, JoyY]
        """
        # degrees on the circle:
        #     90
        # 180     0/360
        #     270
        if (joystick[0] < 108 or joystick[1] > 148) or (joystick[1] < 108 or joystick[0] > 148):  # correct for no input
            angle = int(math.degrees(math.atan2((joystick[1] - 128), (joystick[0] - 128))) + 180.0)
            if angle <= 180:
                angle += 180.0  # fix orientation of degree circle
            else:
                angle -= 180.0
        else:
            angle = 0

        self.set_tile(angle)

    def process_nunchuck_button(self, buttons):
        """:param buttons: [joyZ, joyC]"""
        self.elapsed_time = time.perf_counter() - self.old_time
        if self.elapsed_time > 0.050:  # introduce 50ms delay to avoid double clicking
            self.old_time = time.perf_counter()
            if buttons[0]:
                # Z button from joystick (comparable to left-click)
                self.move_player(self.get_selected_tile())
            elif buttons[1]:
                # C button from joystick (comparable to right-click)
                self.build_mine(self.get_selected_tile())

    def process_mouse_movement(self, pos):
        """
        Processes the input data from the mouse
        :param pos: [MouseX, MouseY]
        """
        # detect where mouse is in relation to player
        # degrees on the circle:
        #     90
        # 180     0/360
        #     270
        playerPos = self.player.get_player_position()
        if math.sqrt(pow((playerPos[0] - pos[0]), 2) + pow((playerPos[1] - pos[1]), 2)) > 20:  # correct for no input
            angle = int(math.degrees(math.atan2((pos[1] - playerPos[1]), (pos[0] - playerPos[0]))) - 180.0) * -1
            if angle < 180:
                angle += 180.0  # fix orientation of degree circle
            else:
                angle -= 180.0
        else:
            angle = 0

        self.set_tile(angle)
        self.set_looking_direction(angle)

    def process_mouse_button(self, button):
        """:param button: mouseButton"""
        if button == MouseButton.left:
            # left-click
            self.move_player(self.get_selected_tile())
        elif button == MouseButton.right:
            # right-click
            self.build_mine(self.get_selected_tile())

    def set_tile(self, angle):
        """
        calculate selected tile from angle
        """

        # if the player is walking then don't highlight a new tile
        if self.player.is_walking:
            return

        # neighbours are arranged in the following manner: [0]=top-right, [1]=top, [2]=top-left,
        # [3]=bottom-left, [4]=bottom, [5]=bottom-right.
        # so starting from the right going counter clockwise

        if 0 <= angle < 60:  # top right
            self.selected_tile = 0
        elif 60 <= angle < 120:  # top
            self.selected_tile = 1
        elif 120 <= angle < 180:  # top left
            self.selected_tile = 2
        elif 180 <= angle < 240:  # bottom left
            self.selected_tile = 3
        elif 240 <= angle < 300:  # bottom
            self.selected_tile = 4
        elif 300 <= angle < 360:  # bottom right
            self.selected_tile = 5
        else:
            self.selected_tile = 0  # fallback selection

        # if newly selected tile, highlight / selected that tile (visually)
        if self.prev_selected_tile != self.selected_tile:
            deselected_tile = self.get_tile(self.prev_selected_tile)
            deselected_tile.unselect_tile()
            selected_tile = self.get_selected_tile()
            selected_tile.select_tile()
            self.prev_selected_tile = self.selected_tile

    def set_looking_direction(self, angle):
        if angle > 300 or angle <= 120:
            self.player.set_look_direction('left')
        else:
            self.player.set_look_direction('right')

    def move_player(self, tile: Tile):
        self.player.move_player(tile)
        self.prev_selected_tile = -1

    def build_mine(self, tile):
        self.player.mine_build(tile)

    def get_selected_tile(self):
        return self.player.get_current_tile().get_neighbours()[self.selected_tile]

    def get_tile(self, index):
        return self.player.get_current_tile().get_neighbours()[index]

