import pygame
from Screen import Screen
from Field import Field
from Player import Player
import time


class program:

    def __init__(self):
        # self.screen = Screen(584, 592, self.loop, title="Test Terrain")
        self.screen = Screen(0, 0, self.loop, title="Test Terrain")

        self.field = Field(self.screen, field_pos=(0, 0), hex_width='auto', field_size=(self.screen.get_size()), hex_amount=(75, 0))
        self.player = Player(self.screen, field_size=(self.screen.get_size()), field=self.field, hex_amount=(75, 39))  # need to implement hex calculation in class

        self.screen.start()

    def loop(self):
        self.screen.background(139, 69, 19)
        self.field.display()
        self.player.display()


if __name__ == '__main__':
    program()
