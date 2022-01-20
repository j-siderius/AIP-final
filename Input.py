import math
from settings import *


class Input:
    def __init__(self):
        """
        Processes all the different inputs into usable variables
        """
        pass

    def process_nunchuck(self, joystick, buttons):
        """
        Processes the serial data from the connected controller
        joystick format: [JoyX, JoyY], [JoyZ, JoyC]
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

        tile = self.set_tile(self, angle)

        if buttons[0]:
            # Z button from joystick (comparable to left-click)
            self.move_player(self, tile)
        elif buttons[1]:
            # C button from joystick (comparable to right-click)
            self.build_mine(self, tile)

        # # # process button clicks here ^^

    def process_mouse(self, pos, button, playerPos):
        """
        Processes the input data from the mouse
        data format: [MouseX, MouseY], button
        """
        # detect where mouse is in relation to player
        # degrees on the circle:
        #     90
        # 180     0/360
        #     270
        if math.sqrt(pow((playerPos[0] - pos[0]), 2) + pow((playerPos[1] - pos[1]), 2)) > 20:  # correct for no input
            angle = int(math.degrees(math.atan2((pos[1] - playerPos[1]), (pos[0] - playerPos[0]))) - 180.0) * -1
            if angle < 180:
                angle += 180.0  # fix orientation of degree circle
            else:
                angle -= 180.0
        else:
            angle = 0

        tile = self.set_tile(self, angle)

        if button == MouseButton.left:
            # left-click
            self.move_player(self, tile)
        elif button == MouseButton.right:
            # right-click
            self.build_mine(self, tile)

        # # # process button clicks here ^^

    def set_tile(self, angle):
        """
        calculate selected tile from angle
        """
        # points are arranged in the following manner: [0]=bottom-right,
        # [1]=bottom-left, [2]=middle-left, [3]=top-left, [4]=top-right, [5]=middle-right. aka, starting right and
        # then clockwise.
        if 330 > angle >= 270:
            # BOTTOM RIGHT
            selected_tile = 0
        elif 270 > angle >= 210:
            # BOTTOM LEFT
            selected_tile = 1
        elif 210 > angle >= 150:
            # MIDDLE LEFT
            selected_tile = 2
        elif 150 > angle >= 90:
            # TOP LEFT
            selected_tile = 3
        elif 90 > angle >= 30:
            # TOP RIGHT
            selected_tile = 4
        elif 30 > angle >= 330:
            # MIDDLE RIGHT
            selected_tile = 5
        else:
            selected_tile = 5  # should design more robust fallback when error
        return selected_tile

    def move_player(self, tile):
        # check if move is allowed
        # do moving stuff
        pass

    def build_mine(self, tile):
        # check if allowed
        # check if mining or building
        # do miney or buildy stuff
        pass

    def update(self):
        pass

